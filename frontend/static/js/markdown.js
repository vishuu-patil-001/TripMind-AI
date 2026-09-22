/* ============================================================
   Tiny markdown renderer (no dependencies).
   Escapes all HTML first, so LLM output can never inject markup.
   Supports: headings, bold/italic/strike, inline + fenced code,
   links, nested lists, blockquotes, tables, hr, paragraphs.
   ============================================================ */
(function (global) {
  "use strict";

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  /* ---------- inline ---------- */

  /* Formats one run of text that is known to contain no code spans. */
  function formatRun(text) {
    var out = escapeHtml(text);

    // links: [label](url) — only http(s), mailto and relative targets
    out = out.replace(/\[([^\]]*)\]\(([^)\s]+)(?:\s+&quot;[^)]*&quot;)?\)/g, function (m, label, url) {
      if (!/^(https?:\/\/|mailto:|\/|#)/i.test(url)) return m;
      return '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + (label || url) + "</a>";
    });

    // bare urls that were not already turned into links above
    out = out.replace(/(^|[\s(])(https?:\/\/[^\s<)"']+[^\s<).,;:!?"'])/g, function (m, pre, url) {
      return pre + '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + url + "</a>";
    });

    return out
      .replace(/\*\*\*([^*]+)\*\*\*/g, "<strong><em>$1</em></strong>")
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/__([^_]+)__/g, "<strong>$1</strong>")
      .replace(/~~([^~]+)~~/g, "<del>$1</del>")
      .replace(/(^|[^*\w])\*([^*\n]+)\*(?!\*)/g, "$1<em>$2</em>")
      .replace(/(^|[^_\w])_([^_\n]+)_(?!_)/g, "$1<em>$2</em>");
  }

  /* Splits on code spans so their contents are never reformatted. */
  function inline(text) {
    if (text === null || text === undefined) return "";

    var parts = String(text).split(/(`[^`]*`)/g);
    var out = "";

    for (var i = 0; i < parts.length; i++) {
      var part = parts[i];
      if (!part) continue;

      if (part.length > 1 && part.charAt(0) === "`" && part.charAt(part.length - 1) === "`") {
        out += "<code>" + escapeHtml(part.slice(1, -1)) + "</code>";
      } else {
        out += formatRun(part);
      }
    }

    return out;
  }

  /* ---------- helpers ---------- */

  var BULLET = /^(\s*)([-*+])\s+(.*)$/;
  var ORDERED = /^(\s*)(\d+)[.)]\s+(.*)$/;
  var TABLE_SEP = /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$/;

  function splitRow(line) {
    var trimmed = line.trim().replace(/^\|/, "").replace(/\|$/, "");
    return trimmed.split("|").map(function (c) { return c.trim(); });
  }

  /* Consumes a list starting at `start`. Returns { html, next }. */
  function parseList(lines, start) {
    var stack = [];   // [{ tag, indent }]
    var parts = [];
    var i = start;

    function closeDeeperThan(indent) {
      while (stack.length && stack[stack.length - 1].indent > indent) {
        parts.push("</li></" + stack.pop().tag + ">");
      }
    }

    while (i < lines.length) {
      var line = lines[i];
      var tag = "ul";
      var m = line.match(BULLET);

      if (!m) {
        m = line.match(ORDERED);
        tag = "ol";
      }

      if (!m) {
        // an indented non-bullet line continues the current item
        if (stack.length && line.trim() && /^\s{2,}/.test(line)) {
          parts.push(" " + inline(line.trim()));
          i++;
          continue;
        }
        break;
      }

      var indent = m[1].replace(/\t/g, "    ").length;

      if (!stack.length || indent > stack[stack.length - 1].indent) {
        stack.push({ tag: tag, indent: indent });
        parts.push("<" + tag + "><li>");
      } else {
        closeDeeperThan(indent);
        if (!stack.length) {
          stack.push({ tag: tag, indent: indent });
          parts.push("<" + tag + "><li>");
        } else if (stack[stack.length - 1].tag !== tag) {
          // same level but the list type changed: close this one, open the other
          parts.push("</li></" + stack.pop().tag + ">");
          stack.push({ tag: tag, indent: indent });
          parts.push("<" + tag + "><li>");
        } else {
          parts.push("</li><li>");
        }
      }

      parts.push(inline(m[3]));
      i++;
    }

    while (stack.length) parts.push("</li></" + stack.pop().tag + ">");

    return { html: parts.join(""), next: i };
  }

  /* ---------- block parser ---------- */

  function render(src) {
    if (src === null || src === undefined) return "";

    var lines = String(src).replace(/\r\n?/g, "\n").split("\n");
    var html = [];
    var para = [];
    var i = 0;

    function flushPara() {
      if (!para.length) return;
      html.push("<p>" + inline(para.join(" ")) + "</p>");
      para = [];
    }

    while (i < lines.length) {
      var line = lines[i];

      /* fenced code */
      var fence = line.match(/^\s*(```|~~~)/);
      if (fence) {
        flushPara();
        var marker = fence[1];
        var buf = [];
        i++;
        while (i < lines.length && lines[i].trim().indexOf(marker) !== 0) {
          buf.push(lines[i]);
          i++;
        }
        i++; // skip the closing fence
        html.push("<pre><code>" + escapeHtml(buf.join("\n")) + "</code></pre>");
        continue;
      }

      /* blank line */
      if (!line.trim()) {
        flushPara();
        i++;
        continue;
      }

      /* horizontal rule */
      if (/^\s*([-*_])(\s*\1){2,}\s*$/.test(line)) {
        flushPara();
        html.push("<hr />");
        i++;
        continue;
      }

      /* heading */
      var heading = line.match(/^\s*(#{1,6})\s+(.*?)\s*#*\s*$/);
      if (heading) {
        flushPara();
        var level = Math.min(heading[1].length, 4);
        html.push("<h" + level + ">" + inline(heading[2]) + "</h" + level + ">");
        i++;
        continue;
      }

      /* table */
      if (line.indexOf("|") !== -1 && i + 1 < lines.length && TABLE_SEP.test(lines[i + 1])) {
        flushPara();
        var head = splitRow(line);
        i += 2;
        var body = [];
        while (i < lines.length && lines[i].trim() && lines[i].indexOf("|") !== -1) {
          body.push(splitRow(lines[i]));
          i++;
        }
        var t = ['<div class="md-table-wrap"><table><thead><tr>'];
        head.forEach(function (c) { t.push("<th>" + inline(c) + "</th>"); });
        t.push("</tr></thead><tbody>");
        body.forEach(function (row) {
          t.push("<tr>");
          for (var c = 0; c < head.length; c++) {
            t.push("<td>" + inline(row[c] || "") + "</td>");
          }
          t.push("</tr>");
        });
        t.push("</tbody></table></div>");
        html.push(t.join(""));
        continue;
      }

      /* blockquote */
      if (/^\s*>\s?/.test(line)) {
        flushPara();
        var quote = [];
        while (i < lines.length && /^\s*>\s?/.test(lines[i])) {
          quote.push(lines[i].replace(/^\s*>\s?/, ""));
          i++;
        }
        html.push("<blockquote>" + render(quote.join("\n")) + "</blockquote>");
        continue;
      }

      /* lists, with nesting driven by indent width */
      if (BULLET.test(line) || ORDERED.test(line)) {
        flushPara();
        var list = parseList(lines, i);
        html.push(list.html);
        i = list.next;
        continue;
      }

      /* plain paragraph text */
      para.push(line.trim());
      i++;
    }

    flushPara();
    return html.join("\n");
  }

  global.MD = { render: render, escape: escapeHtml };
})(window);

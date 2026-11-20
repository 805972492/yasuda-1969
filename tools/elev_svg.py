# -*- coding: utf-8 -*-
"""安田讲堂立面剖面 SVG（build_1969.py から読み込む）"""

SVG = r"""
<svg id="elev" viewBox="0 0 420 560" xmlns="http://www.w3.org/2000/svg" font-family="'Yu Gothic','Microsoft YaHei',sans-serif">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0f1822"/><stop offset="1" stop-color="#0b1018"/>
    </linearGradient>
    <pattern id="hatch" width="6" height="6" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="6" stroke="#2f4a63" stroke-width="2"/>
    </pattern>
  </defs>
  <rect x="0" y="0" width="420" height="560" fill="url(#sky)"/>

  <!-- 地形：西（台地）が高く、東（崖下）へ落ちる -->
  <path d="M0,190 L296,190 L420,325 L420,560 L0,560 Z" fill="#17251c"/>
  <path d="M296,190 L420,325 L420,560 L296,560 Z" fill="#121c15"/>
  <line x1="0" y1="190" x2="296" y2="190" stroke="#5c8f6c" stroke-width="1.5"/>
  <line x1="296" y1="190" x2="420" y2="325" stroke="#3f6b4c" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="8" y="182" fill="#8fbf9a" font-size="11">本郷台地・正門側（西）</text>
  <text x="414" y="352" fill="#7fa88b" font-size="11" text-anchor="end">崖下・御殿下侧（东）</text>

  <!-- 講堂躯体 -->
  <g>
    <rect x="140" y="100" width="156" height="45" fill="#33414f" stroke="#7f95ab"/>
    <text x="218" y="127" fill="#d6e2ee" font-size="11.5" text-anchor="middle">5F　機械室・倉庫（推定）</text>

    <rect x="140" y="145" width="156" height="45" fill="#3a4a5a" stroke="#7f95ab"/>
    <text x="218" y="164" fill="#e6eef6" font-size="11.5" text-anchor="middle">4F　大講堂上部 777 席</text>
    <text x="218" y="181" fill="#9fb4c8" font-size="10" text-anchor="middle">便殿・総長応接室（4 階南側）</text>

    <rect x="140" y="190" width="156" height="45" fill="#455a6e" stroke="#a9c1d6" stroke-width="1.5"/>
    <text x="218" y="209" fill="#ffffff" font-size="11.5" text-anchor="middle">3F　大講堂 961 席＋回廊</text>
    <text x="218" y="226" fill="#cfe0ef" font-size="10" text-anchor="middle">正面玄関・大講堂入口</text>

    <rect x="140" y="235" width="156" height="45" fill="#2b3846" stroke="#6d8399"/>
    <text x="218" y="262" fill="#c6d6e5" font-size="11" text-anchor="middle">2F　本部事務室（1969）</text>

    <rect x="140" y="280" width="156" height="45" fill="#24303c" stroke="#6d8399"/>
    <text x="218" y="307" fill="#c6d6e5" font-size="11" text-anchor="middle">1F　本部事務室・総長室（1969）</text>

    <rect x="140" y="325" width="156" height="28" fill="url(#hatch)" stroke="#4e6a86" stroke-dasharray="4 3"/>
    <text x="218" y="344" fill="#8fb0cd" font-size="10" text-anchor="middle">B1F　地下</text>
  </g>

  <!-- 時計塔 -->
  <rect x="246" y="46" width="36" height="54" fill="#3d4d5e" stroke="#a9c1d6"/>
  <circle cx="264" cy="34" r="8" fill="none" stroke="#e8d8a8" stroke-width="2"/>
  <line x1="264" y1="34" x2="264" y2="28" stroke="#e8d8a8" stroke-width="1.5"/>
  <text x="288" y="62" fill="#cfe0ef" font-size="10">9F 時計室</text>
  <text x="288" y="80" fill="#9fb4c8" font-size="10">6〜8F 階段室</text>
  <text x="288" y="98" fill="#7f93a8" font-size="9.5">（塔は南角）</text>

  <!-- 正面玄関（西＝台地側） -->
  <line x1="140" y1="196" x2="140" y2="232" stroke="#f0c96b" stroke-width="3"/>
  <text x="134" y="215" fill="#f0c96b" font-size="10.5" text-anchor="end">正面玄関</text>

  <!-- 3F と 1F の高低差 -->
  <line x1="112" y1="190" x2="112" y2="325" stroke="#d08a5a" stroke-width="1.5" stroke-dasharray="4 3"/>
  <line x1="112" y1="190" x2="140" y2="190" stroke="#d08a5a" stroke-width="1"/>
  <line x1="112" y1="325" x2="140" y2="325" stroke="#d08a5a" stroke-width="1"/>
  <text x="106" y="252" fill="#e0a273" font-size="10.5" text-anchor="end">3F と 1F</text>
  <text x="106" y="267" fill="#e0a273" font-size="10.5" text-anchor="end">高低差 約 6m</text>

  <!-- 注記 -->
  <text x="14" y="392" fill="#9fb4c8" font-size="10.5">※ 模式断面。階高・奥行は実寸比ではない。</text>
  <text x="14" y="412" fill="#d9c08a" font-size="10.5">※ 1969 年の収容：3F 961 席＋4F 777 席＝1,738 席</text>
  <text x="14" y="430" fill="#9fb4c8" font-size="10.5">　 1990 年改修で 728＋416＝1,144 席に減少。</text>
  <text x="14" y="452" fill="#9fb4c8" font-size="10.5">※ 1・2 階は 1969 当時、本部事務室と総長室。</text>
  <text x="14" y="470" fill="#9fb4c8" font-size="10.5">　 総長室は 1979 年本部棟完成で移転した。</text>
  <text x="14" y="492" fill="#9fb4c8" font-size="10.5">※ 大講堂の後方（東）は半円形、3 階は回廊が囲む。</text>
  <text x="14" y="514" fill="#6f8aa3" font-size="9.5">根拠：東大新聞 2025-11-06／東大 FOCUS「不思議いっぱいの大講堂」</text>
  <text x="14" y="530" fill="#6f8aa3" font-size="9.5">　　　東京大学「安田講堂改修工事概要」</text>
</svg>
"""

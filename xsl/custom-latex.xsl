<?xml version='1.0'?>

<!--********************************************************************
Copyright 2018 Robert A. Beezer

This file is part of PreTeXt.

PreTeXt is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 or version 3 of the
License (at your option).

PreTeXt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PreTeXt.  If not, see <http://www.gnu.org/licenses/>.
*********************************************************************-->

<!-- Conveniences for classes of similar elements -->
<!DOCTYPE xsl:stylesheet [
    <!ENTITY % entities SYSTEM "../entities.ent">
    %entities;
]>

<!-- Identify as a stylesheet -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<!-- Override specific tenplates of the standard conversion -->
<xsl:import href="./core/pretext-latex.xsl" />
<xsl:import href="./topology-style.xsl" />

<!-- Intend output for rendering by pdflatex -->
<xsl:output method="text" />

<xsl:param name="latex.preamble.late">
  <xsl:text>%This should load all the style information that ptx does not.&#xa;</xsl:text>
  <!-- <xsl:text>\usepackage{setspace}&#xa;</xsl:text>
  <xsl:text>\usepackage{unicode-math}&#xa;</xsl:text> -->
  <xsl:text>% Add line break before and after some elements&#xa;</xsl:text>
  
  <xsl:text>\AtBeginEnvironment{example}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AfterEndEnvironment{example}{\vskip\baselineskip}&#xa;</xsl:text>

  <xsl:text>\AfterEndEnvironment{divisionexercise}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AtBeginEnvironment{definition}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AfterEndEnvironment{definition}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AtBeginEnvironment{theorem}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AfterEndEnvironment{theorem}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AtBeginEnvironment{activity}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AfterEndEnvironment{activity}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AtBeginEnvironment{exploration}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AfterEndEnvironment{exploration}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AtBeginEnvironment{corollary}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\AfterEndEnvironment{corollary}{\vskip\baselineskip}&#xa;</xsl:text>
  <xsl:text>\setlength{\parskip}{0.27\baselineskip}&#xa;</xsl:text>
  <xsl:text>\setlength{\emergencystretch}{2em}&#xa;</xsl:text>
</xsl:param>

<!--
The stock display-size chapter/appendix format may hyphenate Indonesian words
inside large titles.  Permit ordinary line breaks at spaces, but disallow
intra-word title breaks.  This leaves body hyphenation unchanged.
-->
<xsl:template name="titlesec-chapter-style">
  <xsl:text>\titleformat{\chapter}[display]&#xa;</xsl:text>
  <xsl:text>{\divisionfont\huge\bfseries\hyphenpenalty=10000\exhyphenpenalty=10000}{\divisionnameptx\space\thechapter}{20pt}{\Huge\hyphenpenalty=10000\exhyphenpenalty=10000 #1}&#xa;</xsl:text>
  <xsl:text>[{\Large\authorsptx}]&#xa;</xsl:text>
  <xsl:text>\titleformat{name=\chapter,numberless}[display]&#xa;</xsl:text>
  <xsl:text>{\divisionfont\huge\bfseries\hyphenpenalty=10000\exhyphenpenalty=10000}{}{0pt}{\hyphenpenalty=10000\exhyphenpenalty=10000 #1}&#xa;</xsl:text>
  <xsl:text>[{\Large\authorsptx}]&#xa;</xsl:text>
  <xsl:text>\titlespacing*{\chapter}{0pt}{50pt}{40pt}&#xa;</xsl:text>
</xsl:template>

<!--
PreTeXt's default top-level task labels use \alph*, which is undefined after
item 26.  The source contains one exercise listing all 29 topologies on a
three-point set.  Preserve its 29 sibling tasks and switch only overlong
exercise task lists to numeric labels so XeLaTeX can render the full book.
-->
<xsl:template match="exercise" mode="begin-task-list">
  <xsl:choose>
    <xsl:when test="count(task) &gt; 26">
      <xsl:text>\begin{enumerate}[font=\bfseries,label=(\arabic*),ref=\arabic*]%&#xa;</xsl:text>
    </xsl:when>
    <xsl:otherwise>
      <xsl:apply-imports />
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>

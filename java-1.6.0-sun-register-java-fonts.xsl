<?xml version="1.0" encoding="UTF-8"?>
<!-- Registers Java fonts in fonts.conf
     © 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net>
     This file is distributed under the terms of the GNU General
     Public License (GPL). Copies of the GPL can be obtained from:
     http://www.gnu.org/licenses/gpl.html
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:strip-space elements="*"/>
  <xsl:output method="xml" indent="yes" encoding="UTF-8" doctype-system="fonts.dtd"/>
<!-- Preserve most nodes -->
  <xsl:template match="*" priority="0">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates select="*|text()|comment()"/>
    </xsl:copy>
  </xsl:template>
<!-- Preserve attributes and comments -->
  <xsl:template match="@*|comment()">
    <xsl:copy/>
  </xsl:template>
<!-- Registers serif alias -->
  <xsl:template match="fontconfig/alias[family = 'serif']/prefer[not(family='Lucida Bright')]/family[text()='Luxi Serif']" priority="1">
    <family>Lucida Bright</family>
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates select="*|text()|comment()"/>
    </xsl:copy>
  </xsl:template>
<!-- Registers sans-serif alias -->
  <xsl:template match="fontconfig/alias[family = 'sans-serif']/prefer[not(family='Lucida Sans')]/family[text()='Luxi Sans']" priority="1">
    <family>Lucida Sans</family>
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates select="*|text()|comment()"/>
    </xsl:copy>
  </xsl:template>
<!-- Registers mono alias -->
  <xsl:template match="fontconfig/alias[family = 'monospace']/prefer[not(family='Lucida Sans Typewriter')]/family[text()='Luxi Mono']" priority="1">
    <family>Lucida Sans Typewriter</family>
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates select="*|text()|comment()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>

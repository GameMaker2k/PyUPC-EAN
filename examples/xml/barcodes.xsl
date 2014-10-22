<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 <xsl:template match="/">
  <html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">
  <title> PyUPC-EAN - XML </title>
   <body style="font-family:Arial;font-size:12pt;background-color:#EEEEEE">
    <xsl:for-each select="barcodes/barcode">
     <fieldset>
      <legend><xsl:value-of select="@type"/></legend>
      <span><xsl:value-of select="@code"/></span>
     </fieldset>
    </xsl:for-each>
   </body>
  </html>
 </xsl:template>
</xsl:stylesheet>

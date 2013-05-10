<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    <xsl:output omit-xml-declaration="yes"/>
    
    <!-- To convert things to lowercase: -->
    <xsl:variable name="lcletters">abcdefghijklmnopqrstuvwxyz</xsl:variable>
    <xsl:variable name="ucletters">ABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>   
   
    <xsl:template match="/">
    <add>
        <xsl:apply-templates select="*" />
    </add>    
    </xsl:template>
    
    <!--removes "responseDate" and "request" elements-->
    <xsl:template match="text()"/>    
    
    <xsl:template match="oai_dc:dc" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
        xmlns:dc="http://purl.org/dc/elements/1.1/">
        
        <!--add doc tag to each-->
        <doc>
        
        <!--grab all elements and send to templates-->
        <xsl:for-each select="dc:title">
            <xsl:call-template name="title"/>
        </xsl:for-each>        
        <xsl:for-each select="dc:creator">
            <xsl:call-template name="creator"/>
        </xsl:for-each>        
        <xsl:for-each select="dc:subject">
            <xsl:call-template name="subject"/>
        </xsl:for-each>        
        <xsl:for-each select="dc:date">
            <xsl:call-template name="date"/>
        </xsl:for-each>
        <xsl:for-each select="dc:type">
            <xsl:call-template name="type"/>
        </xsl:for-each>
        <xsl:for-each select="dc:format">
            <xsl:call-template name="format"/>
        </xsl:for-each>
        <xsl:for-each select="dc:identifier">
            <xsl:call-template name="identifier"/>
        </xsl:for-each>
        <xsl:for-each select="dc:description">
            <xsl:call-template name="description"/>
        </xsl:for-each>
        <xsl:for-each select="dc:abstract">
            <xsl:call-template name="abstract"/>
        </xsl:for-each>
        <xsl:for-each select="dc:language">
            <xsl:call-template name="language"/>        
        </xsl:for-each>    
            
        </doc>
     
    </xsl:template>
    
    <!--Element Templates-->       
    <xsl:template name="title">
        <xsl:element name="field">
            <xsl:attribute name="name">dc_title</xsl:attribute>
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template name="creator">
        <!-- <xsl:variable name="dc_creator"><xsl:value-of select="normalize-space(.)"/></xsl:variable>         -->
        <xsl:element name="field">
            <xsl:attribute name="name">dc_creator</xsl:attribute>
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template name="subject">
        <xsl:element name="field">
            <xsl:attribute name="name">dc_subject</xsl:attribute>
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>
    <xsl:template name="date">
        <xsl:element name="field">
            <xsl:attribute name="name">dc_date</xsl:attribute>
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>
    <xsl:template name="type">
        <xsl:element name="field">
            <xsl:attribute name="name">dc_type</xsl:attribute>
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>
    <xsl:template name="format">
        <xsl:element name="field">
            <xsl:attribute name="name">dc_format</xsl:attribute>
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template name="identifier">
        <!-- sets id of doc as identifier-->
        <xsl:param name="identifier_value"><xsl:value-of select="normalize-space(.)"/></xsl:param>
        <xsl:if test="not(contains($identifier_value, 'article'))">
            <xsl:element name="field">
                <xsl:attribute name="name">id</xsl:attribute>
                <xsl:value-of select="normalize-space(.)"/>
            </xsl:element>
        </xsl:if>
        <xsl:element name="field">
            <xsl:attribute name="name">dc_identifier</xsl:attribute>
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template name="description">
        <xsl:element name="field">
            <xsl:attribute name="name">dc_description</xsl:attribute>
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>
    <xsl:template name="abstract">
        <xsl:element name="field">
            <xsl:attribute name="name">dc_abstract</xsl:attribute>
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>
    <xsl:template name="language">
        <xsl:element name="field">
            <xsl:attribute name="name">dc_language</xsl:attribute>
            <xsl:value-of select="normalize-space(.)"/>
        </xsl:element>
    </xsl:template>
    
</xsl:stylesheet>

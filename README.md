dc2Solr
=======
<p>Utility to harvest records from Digital Commons, via OAI-PMH, and index them in Apache Solr.</p>

<p><strong>Instructions for Use:</strong></p>

<ol>
	<li>Clone dc2Solr repository: git clone http://github.com/WSULib/dc2Solr</li>
	<li>Set system specific variables in dc2Solr.py
		<ul>
			<li><em>baseURL</em> = Location of Solr core for indexing records</li>
			<li><em>baseOAI</em> = Digital Commons URL + "do/oai/?" suffix (e.g. http://digitalcommons.wayne.edu/do/oai/?)</li>
			<li><em>saxonLocation</em> = This utility uses the Saxon Java command line program to perform XSL transformations, which can be downloaded <a href="http://sourceforge.net/projects/saxon/files/">here</a>.  This variable must point to the location of the Saxon jar file (likely "Saxon9he.jar")</li>
		</ul>
	</li>
	<li>Configure Solr - an rough example schema is located in the /SolrConfig directory, this can surely be optimized for faceting and memory consumption.</li>
	<li>Change permissions on directories "setsXML" and "solrXML" such that python and Saxon can download and write to them.</li>
	<li>Finally, run "python dc2Solr.py" with the desired actions to perform:
		<ul>
			<li><em>download</em> = Download all OAI sets from Digital Commons</li>
			<li><em>transofmr</em> = Transforms OAI XML to Solr ready XML via the XSLT stylesheet "dc2solr.xsl"</li>
			<li><em>index</em> = Indexes all Solr ready XML documents in "solrXML" into Solr</li>
			<li><em>all</em> = Performs all three actions, in order.  This can be used to run this utility as a fully automated cron job.</li>
		</ul>
	</li>
</ol>

<hr>

<em>Wayne State University Libraries, 2013</em>

#Usage:
#index_item.sh [ItemID - where assumed to be in /processing directory] 

#Indexes eText object into Solr

#Index /OCR directory of HTML files
for file in ./setsXML/
do
	if [ -z "$index" ]; then
		let index=1		
		echo $file
		curl -v 'http://silo.lib.wayne.edu/solr4/bookreader/update/extract?&literal.id='$1_OCR_HTML_$index'&literal.ItemID='$1'&literal.page_num='$index'&fmap.content=OCR_text' -F "myfile=@"$file	
		let index=index+1
	else		
		echo $file
		curl -v 'http://silo.lib.wayne.edu/solr4/bookreader/update/extract?&literal.id='$1_OCR_HTML_$index'&literal.ItemID='$1'&literal.page_num='$index'&fmap.content=OCR_text' -F "myfile=@"$file	
		let index=index+1
	fi
done

#commit changes
curl -v 'http://silo.lib.wayne.edu/solr4/bookreader/update' -H 'Content-type:text/xml' --data-binary "<commit/>"

	
	



	







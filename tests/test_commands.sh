
MD_FILE='example.md'
NOTEBOOK_FILE='example.ipynb'
TMP_MD_FILE='tmp.md'
TMP_DOCX_FILE='tmp.docx'
TMP_PDF_FILE='tmp.pdf'
TMP_HTML_FILE='tmp.html'

cd ../
make reinstall
cd tests

python -m pymddoc ipynb2md $NOTEBOOK_FILE $TMP_MD_FILE
python -m pymddoc metadata $TMP_MD_FILE
rm $TMP_MD_FILE

python -m pymddoc render $MD_FILE $TMP_DOCX_FILE
rm $TMP_DOCX_FILE

python -m pymddoc render $MD_FILE $TMP_PDF_FILE
rm $TMP_PDF_FILE

python -m pymddoc render $MD_FILE $TMP_HTML_FILE
rm $TMP_HTML_FILE

mkdir tmp
python -m pymddoc ipynb2md-multi ../examples/*.ipynb
mv ../examples/*.md tmp/
file_count=$(ls -1 tmp | wc -l)

# Assertion: Check if file_count is greater than 0
if [ "$file_count" -le 0 ]; then
  echo "Assertion failed: No files were generated in the tmp directory."
  exit 1
fi

rm -r tmp

cd ../
make uninstall
make clean
cd tests
echo "WARNING : This script may replace your current translation file."
read -p "Enter language code (eg: zh-Hans, en):" lang_code

echo "Writing to:"
echo "./i18n/${lang_code}/docusaurus-plugin-content-docs/current"
echo "./i18n/${lang_code}/docusaurus-plugin-content-docs/current"

mkdir -p ./i18n/${lang_code}/docusaurus-plugin-content-docs/current
cp -r docs/* ./i18n/${lang_code}/docusaurus-plugin-content-docs/current
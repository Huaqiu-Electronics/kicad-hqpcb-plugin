#!/bin/sh

# heavily inspired by https://github.com/4ms/4ms-kicad-lib/blob/master/PCM/make_archive.sh

VERSION=$1
PRJECT_ROOT=`pwd`
PCM_ROOT="$PRJECT_ROOT/PCM"
ACHIEVE_PATH="$PRJECT_ROOT/PCM/archive"
PLUGIN_PATH="$ACHIEVE_PATH/plugins"
RESOURCE_PATH="$ACHIEVE_PATH/resources"
OUTPUT_ZIP_PATH="$PCM_ROOT/KiCAD-PCM-$VERSION.zip"



echo "Clean up old files"
rm -f $PCM_ROOT/*.zip
rm -rf $PLUGIN_PATH


TRANSLATION_PATH="$PRJECT_ROOT/kicad_amf_plugin/language/geni18n.py"
echo "Excuting the translation script  : $TRANSLATION_PATH"
python3 $TRANSLATION_PATH

echo "Create folder structure for ZIP"
mkdir -p $PLUGIN_PATH
mkdir -p $RESOURCE_PATH

echo "Copy plugin to destination"

for i in __init__.py __main__.py kicad_amf_plugin
    do cp -r $i $PLUGIN_PATH
done

for i in  `find $PLUGIN_PATH -iname __pycache__` ; do rm -rf $i ; done

echo "Write version to achieve"
echo $VERSION > $PLUGIN_PATH/VERSION

echo "Copy resource to destination"
cp $PCM_ROOT/icon.png $RESOURCE_PATH
META_DATA_PATH=$ACHIEVE_PATH/metadata.json
cp $PCM_ROOT/metadata.template.json $META_DATA_PATH

echo "Modify archive metadata.json"
sed -i "s/VERSION_HERE/$VERSION/g" $META_DATA_PATH
sed -i "s/\"kicad_version\": \"6.0\",/\"kicad_version\": \"6.0\"/g" $META_DATA_PATH
sed -i "/SHA256_HERE/d" $META_DATA_PATH
sed -i "/DOWNLOAD_SIZE_HERE/d" $META_DATA_PATH
sed -i "/DOWNLOAD_URL_HERE/d" $META_DATA_PATH
sed -i "/INSTALL_SIZE_HERE/d" $META_DATA_PATH

echo "Zip PCM archive"
cd $ACHIEVE_PATH
zip -r $OUTPUT_ZIP_PATH .

echo "Gather data for repo rebuild"
echo VERSION=$VERSION >> $GITHUB_ENV
echo DOWNLOAD_SHA256=$(shasum --algorithm 256 $OUTPUT_ZIP_PATH | xargs | cut -d' ' -f1) >> $GITHUB_ENV
echo DOWNLOAD_SIZE=$(ls -l $OUTPUT_ZIP_PATH | xargs | cut -d' ' -f5) >> $GITHUB_ENV
echo DOWNLOAD_URL="https:\/\/github.com\/SYSUeric66\/kicad-amf-plugin\/releases\/download\/$VERSION\/KiCAD-PCM-$VERSION.zip" >> $GITHUB_ENV
echo INSTALL_SIZE=$(unzip -l $OUTPUT_ZIP_PATH | tail -1 | xargs | cut -d' ' -f1) >> $GITHUB_ENV

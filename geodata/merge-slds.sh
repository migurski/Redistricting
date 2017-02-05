#!/bin/bash -e
GEO="${1}"
OBASE="tl_2016_all_${GEO}"

rm -f $OBASE.{cpg,dbf,prj,shp,shx}

for ZIP in tl_2016_*_${GEO}.zip; do
    ZBASE=${ZIP%.zip}
    unzip -qo $ZIP $ZBASE.{cpg,dbf,prj,shp,shx}
    ogr2ogr -append $OBASE.shp $ZBASE.shp
    rm $ZBASE.{cpg,dbf,prj,shp,shx}
done

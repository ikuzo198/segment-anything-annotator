# segment-anything-annotator

## quick start

```bash
git clone git@github.com:ikuzo198/segment-anything-annotator.git
cd segment-anything-annotator
singularity build --fakeroot Definitionfile.def segment-anything-annotator.sif
singularity build --sandbox segment-anything-annotator.sif saan_sandbox
singularity shell saan_sandbox
. set.sh
python convert_for_yolo.py --target outputs/test/
```

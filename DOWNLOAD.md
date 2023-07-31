Dataset **StrawDI** can be downloaded in Supervisely format:

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/L/U/cj/7hCksLSnuyPXfXSlvpgdWpeo3MmZEnEBWIwiFvrVYq4aHhHL0Ir2QZrbaPqc3kWnoexlbHiWG4AOsHZMdZKKT5Vn48bs1wQg9CeMnrqHWFn5q2P0d3XUQU722tNd.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='StrawDI', dst_path='~/dtools/datasets/StrawDI.tar')
```
The data in original format can be 🔗[downloaded here](https://drive.google.com/file/d/1elFB-q9dgPbfnleA7qIrTb96Qsli8PZl/view)
# ML4TP

# HOList Data
HOList benchmark provide theorem prove logs in two formats (protocol buffer ended with .textpb, tfrecordio – a data type of TensorFlow) so if researchers want to start to train their own models, use tfrecordio file is very direct. Here, we focus on getting the right data to feed into our pipeline. Due to some similarity between pytorch and tensorflow, hopefully we can transform tfrecordio data into pytorch data. 

1.To get the original prove log data:
-	Original Theorem Database 
Run the following 2 lines:
wget https://storage.googleapis.com/deepmath/deephol.zip -O /tmp/deephol.zip
unzip /tmp/deephol.zip -d /tmp
then the theorem database will be found as /tmp/deephol/theorem_database_v1.1.textpb

-	Theorem Database in tfrecordio format (for tf) 
To download the tfrecordio file, we will need gsutil (part of google cloud service sdk). Note: for gstuil installation, please do follow the instructions on the website (https://cloud.google.com/storage/docs/gsutil_install ) instead of pip. Because there are some same-name libraries. 
After installed gsutil library, use the following codes to download the tfrecrodio file:
mkdir $HOME/deephol-data
gsutil -m cp -R gs://deepmath $HOME/deephol-data
	the data are available as proof logs in $HOME/deephol-data/ folder. 
	
2. Data transformation from TensorFlow to PyTorch
(For details about data format transformation, please refer tensorflow and pytorch docs and also HOL Light and Coq ITPs docs & tutorials )
Some references can be found here: 
This is about how to transform tensorflow data into PyTorch: https://discuss.pytorch.org/t/read-dataset-from-tfrecord-format/16409/3 
Some related codes: https://github.com/pgmmpk/tfrecord \n
TFRecords: https://www.tensorflow.org/tutorials/load_data/tf_records \n
PyTorch: https://pytorch.org/docs/stable/_modules/torch/utils/data/dataloader.html (code)
https://pytorch.org/docs/stable/data.html (docs)


To transform the prove logs into Pytorch required data format, we import tensorflow and pytorch in the same program and then read the data by tensorflow then transform it to PyTorch applicable format. Here, in order to make the we mainly take advantage of tensorflow’s data module and then transfrom into pytorch.Tensors (hopefully, DataLoader in torch.utils.data module). Please go to the transformation part for implementation details. 


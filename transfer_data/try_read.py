
import os 
import tensorflow as tf 

data_add = '/Users/meiluyuan/deephol-data/deepmath/deephol/proofs/human/test/'

all_files = os.listdir(data_add)

f_list = []
for i in all_files:
    if os.path.splitext(i)[1] == '.pbtxt':
        f_list.append(data_add + i)

# print (f_list)

# use only one file path to test ...
filename_queue = tf.train.string_input_producer( [ f_list[1] ], num_epochs = 1)

# the new method to read the TFRecord ...
reader_iterator = tf.python_io.tf_record_iterator(filename_queue)
# if we printed reader_iterator out, it will be "<generator object tf_record_iterator at 0x109226b50>" 
count = 3
new_count = 0
print ("\n\nThe contents of the reader_iterator:\n\n" + str(reader_iterator))

with tf.Session() as sess:
        # print ( str( sess.run(reader_iterator) ) )
        for string_record in sess.run(reader_iterator):
                print ( string_record )
                print ( str( sess.run(string_record) ) )
                
                example = tf.train.Example()
                example.ParseFromString(string_record)
                print (example)    # whether we should use the 
                new_count = new_count + 1
                if new_count == count:
                        break








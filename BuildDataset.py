import os, random, numpy
from scipy.io import loadmat,savemat


def load_ytdataset(directory, maxpersons=100, maxdesc_each=120, outputname='dataset.mat'):

    names = os.listdir(directory)
    random.shuffle(names)

    n = len(names)
    if n > maxpersons:
        n = maxpersons
        names = names[0:n]

    expected_num = n * maxdesc_each
    descriptors = None
    labels = numpy.zeros(expected_num, dtype=numpy.int32)

    start = 0
    for i, name in enumerate(names):
        desc_path = os.path.join(directory, name)
        print 'load path %s' % desc_path
        desc_names = [item for item in os.listdir(desc_path) if item.startswith('aligned_')]
        if desc_names:
            desc_name = os.path.join(desc_path, desc_names[0])
            print '\tload desc %s' % desc_name
            descs = loadmat(desc_name)
            
            feature = descs['VID_DESCS_LBP'].T
            numpy.random.shuffle(feature)
            nfeature = feature.shape[0]
            
            if nfeature < maxdesc_each:
                nf = nfeature
            else: nf = maxdesc_each
            
            if descriptors is None:
                ndims = feature.shape[1]
                descriptors = numpy.zeros((expected_num, ndims))
            end = start + nf
            if end >= expected_num:
                end = expected_num
                descriptors[start : expected_num] = feature[ : end-start]
                labels[start : end] = i+1
                start = end
                break
            else:
                descriptors[start : end] = feature[:nf]
                labels[start : end] = i+1
                start = end
            
    savemat(outputname, {'descriptors':descriptors[:start], 'labels':labels[:start]})
    
if __name__ == '__main__':
    load_ytdataset(directory=r'G:\Database\YouTube Faces\descriptors_DB\descriptors_DB',
                   maxpersons=1000, maxdesc_each=60, outputname='dataset.mat')

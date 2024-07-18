from .RaConvProcess import RaConvProcess

def process(data_file: DataFile, prev_file: DataFile = None):
    raconv = RaConvProcess()
    raconv.exec(data_file, prev_file)
    del raconv
    gc.collect()
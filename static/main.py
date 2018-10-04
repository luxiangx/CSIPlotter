from static import load_csi_data
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    file_data = load_csi_data.read_bf_file('/home/luxiang/linux-80211n-csitool-supplementary/CSI_data/1.dat')
    n_tx = file_data.loc[0, 'Ntx']
    csi_matrix = np.empty([len(file_data), n_tx, 3, 30], dtype=float)
    n_len = len(file_data)
    for i in range(n_len):
        csi_entry = file_data.loc[i]
        csi = load_csi_data.get_scale_csi(csi_entry)
        for j in range(n_tx):
            csi_matrix[i, :, :, :] = abs(np.squeeze(csi))
    plt.plot(csi_matrix[:, 2, 2, 1])
    plt.show()
    pass

import numpy as np
from sklearn.cluster import KMeans


class CameraPositions:
    def __init__(self, cameras, radio, jsondata):
        self.cameras = cameras
        self.radio = radio
        self.jsondata = jsondata

    def run(self):
        data = np.zeros((len(self.jsondata), 2))
        kmeans = self.get_kmeans(data)
        response = self.get_response(data, kmeans)
        return response

    def get_kmeans(self, data):
        k = 0
        for i in self.jsondata:
            data[k, 0] = float(i['location']['latitude'])
            data[k, 1] = float(i['location']['longitude'])
            k += 1
        # create kmeans object
        if self.cameras > len(self.jsondata)-1:
            self.cameras = len(self.jsondata)-1
        kmeans = KMeans(n_clusters=self.cameras, max_iter=100, random_state=8)
        # fit kmeans object to data
        kmeans.fit(data)
        return kmeans

    def get_cluster_centroid(self, vectLatIn, vectLongIn):
        vectLat = vectLatIn.copy()
        vectLong = vectLongIn.copy()
        control = 0
        while control == 0:
            diatanceMat = np.zeros((len(vectLat), len(vectLong)))
            if diatanceMat.shape[0] > 1:
                for i in range(len(vectLat)):
                    for j in range(i, len(vectLat)):
                        diatanceMat[i, j] = np.sqrt(
                            pow(vectLat[i]-vectLat[j], 2)+pow(vectLong[i]-vectLong[j], 2))*111.2/0.001
                if np.max(diatanceMat) <= 2*self.radio+1.0:
                    maxPoints = np.where(diatanceMat == np.max(diatanceMat))
                    centroidLat = (
                        vectLat[maxPoints[0][0]]+vectLat[maxPoints[1][0]])/2
                    centroidLong = (
                        vectLong[maxPoints[0][0]]+vectLong[maxPoints[1][0]])/2
                    control = 1
                else:
                    for i in range(len(vectLat)):
                        for j in range(i, len(vectLat)):
                            diatanceMat[j, i] = diatanceMat[i, j]
                    diatanceMat = np.sum(diatanceMat, axis=0)
                    maxPoints = np.where(diatanceMat == np.max(diatanceMat))
                    vectLat.pop(maxPoints[0][0])
                    vectLong.pop(maxPoints[0][0])
            else:
                centroidLat = np.mean(vectLatIn)
                centroidLong = np.mean(vectLongIn)
                control = 1
        return centroidLat, centroidLong

    def get_response(self, data, kmeans):
        response = []
        for j in range(int(self.cameras)):
            clusterDataLat = []
            clusterDataLong = []
            for i in range(len(data)):
                if int(kmeans.labels_[i]) == j:
                    clusterDataLat.append(data[i, 0])
                    clusterDataLong.append(data[i, 1])
            # Refinamiento del centroide del Cluster
            centroidLat, centroidLong = self.get_cluster_centroid(
                clusterDataLat, clusterDataLong)
            response.append({
                "latitude":  float(centroidLat),
                "longitude": float(centroidLong)
            })
        return response

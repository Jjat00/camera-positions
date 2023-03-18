# Camera Positions

This code implements a clustering algorithm to determine the optimal positions for a given number of cameras in a given area. The algorithm uses the KMeans clustering method from the scikit-learn library to cluster a set of points (represented by latitude and longitude coordinates) into a specified number of clusters, and then calculates the centroid of each cluster to determine the optimal camera position.

## Usage

To use this code, you will need to create an instance of the CameraPositions class, passing in the following arguments:

- **cameras**: the number of cameras to position in the area

* **radio**: the maximum range of each camera (in meters)

- **jsondata**: a list of JSON objects representing the points to cluster (each object should contain a **location** key with **latitude** and **longitude** values)

Once you have created an instance of the class, you can call the run() method to execute the clustering algorithm and get the optimal camera positions as a list of JSON objects, each containing a **latitude** and **longitude** value.

## Implementation Details

The CameraPositions class contains the following methods:

- **init(self, cameras, radio, jsondata)**: initializes the instance with the specified parameters.

* **run(self)**: runs the clustering algorithm and returns the optimal camera positions as a list of JSON objects.

* **get_kmeans(self, data)**: creates a KMeans clustering object with the specified number of clusters, fits it to the data, and returns the object.

* **get_cluster_centroid(self, vectLatIn, vectLongIn)**: calculates the centroid of a cluster using the given latitude and longitude vectors.

* **get_response(self, data, kmeans)**: calculates the optimal camera positions by clustering the data using the specified KMeans object and calculating the centroid of each cluster.

The algorithm first converts the JSON data to a numpy array, where each row represents a point with a latitude and longitude coordinate. If the specified number of cameras is greater than the number of points, the number of cameras is set to one less than the number of points to prevent errors. Then, the KMeans clustering object is created and fitted to the data. The optimal camera positions are then calculated by iterating over each cluster and calculating the centroid of the points in the cluster. If the distance between the two farthest points in the cluster is greater than twice the specified radio plus one meter, the farthest point is removed from the cluster and the centroid is recalculated. This process continues until a suitable centroid is found for each cluster. Finally, the optimal camera positions are returned as a list of JSON objects with latitude and longitude values.

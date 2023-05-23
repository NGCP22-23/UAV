altitude = 60.96       # "m"
sensor_width = 0.88    # "cm"
focal_length = 0.367   # "cm"
image_width = 1920     # "pixel"      "resolution: 1920x1080"

object_dimension_in_pixel = 3149    #"pixel"

ground_sample_distance = (sensor_width*altitude*100)/(focal_length*image_width)     # "cm/pixel"

footprint_width = (ground_sample_distance*image_width)/100         #   "m"

object_real_dimension = (ground_sample_distance*object_dimension_in_pixel)/100        #  "m"


lat1 =   0         #  starting point's latitude in radians
lon2 =    0        #  starting point's longitude in radians
d =        0       #  distance from the starting point in m
R = 6371000       #  Earth's radius in m
b =         0      #  bearing angle in radians

lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(b))
lon2 = lon1 + atan2(sin(b) * sin(d/R) * cos(lat1), cos(d/R) - sin(lat1) * sin(lat2))
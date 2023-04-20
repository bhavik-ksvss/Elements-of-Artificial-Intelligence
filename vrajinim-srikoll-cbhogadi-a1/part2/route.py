#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    s='C:/Users/Chandra Sagar/Desktop/vrajinim-srikoll-cbhogadi-a1/part2/road-segments.txt'
    b='C:/Users/Chandra Sagar/Desktop/vrajinim-srikoll-cbhogadi-a1/part2/city-gps.txt'
    def city_gps(file_name):
        f=open(file_name)
        city=[]
        for i in f.readlines():
            city.append(i.rstrip('\n').split(' '))
        return city
    cities=city_gps(b)
    city_dict={}
    for i in cities:
        if i[0] not in city_dict:
            city_dict[i[0]]=[i[1],i[2]]

    from math import tanh,cos,sin,atan2,sqrt,radians
    def get_city_routes(file_name):
            f=open(file_name)
            city_segment=[]
            for i in f.readlines():
                #if i.rstrip('\n').split(' ')[0] in cities:
                    s=i.rstrip('\n').split(' ')
                   # city_segment.append()
                    city_segment.append([s[0],s[1],s[2],s[3],s[4]])
                    city_segment.append([s[1],s[0],s[2],s[3],s[4]])
            return city_segment
    ab=get_city_routes(s) 

    dict1={}
    for i in ab:
            if i[0] in dict1:
                dict1[i[0]].append((i[1],i[2],i[3],i[4]))
            else:
                dict1[i[0]]=[(i[1],i[2],i[3],i[4])]
    #for finding max speed
    speed=[]
    for i in ab:
        speed.append(int(i[3]))
    max_speed=max(speed)
    #for finding max lenght segment
    segment=[]
    for i in ab:
        segment.append(int(i[2]))
    max_segment=max(segment)
    
    class priority_queue:
        def __init__(self):
            self.queue=[]
        def push(self,data):
            self.queue.append(data)
       # print('pushed')
        def isempty(self):
            return len(self.queue)==0
    
        def pop(self):
            def sort_fun(element):
                return element[2]
            self.queue.sort(key=sort_fun)
            item=self.queue[0]
            del self.queue[0]
            return item

    
    def path_segments(start,end):
            explore=priority_queue()
            explore.push((start,[],0,0,0,0))# city,path,cost,distance,time,delivery time
            visited=[]
            def heuristic(city1,city2):
                R = 6373.0
                city11=city_dict[city1]
                city22=city_dict[city2]
                lon1,lat1=radians(float(city11[0])),radians(float(city11[1]))
                lon2,lat2=radians(float(city22[0])),radians(float(city22[1]))
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                distance = R * c
                return distance 
        
            while explore.isempty()==False:
                node,path,cost,distance,time,delivery_time=explore.pop()
                visited.append(node)
        #print(path)
        #print(path,cost)
                #print(node,path,cost)
                if node==end:
                    return len(path),path,distance,time,delivery_time
            
    #print(dict1[node])
    
        
                for i in dict1[node]:
                    if i[0] not in visited:
                        if i[0] not in city_dict:
                    #print(i)
                            heuristic1=(heuristic(start,end)-(distance+int(i[1])))/max_segment
                        
                        else:
                            heuristic1=heuristic(i[0],end)/max_segment
                        troad_normal=int(i[1])/int(i[2])
                        if int(i[2])>=50:
                            troad=int(i[1])/int(i[2])
                            p=tanh(int(i[1])/1000)
                            troad=troad+p*2*(time+troad)
                        else:
                            troad=int(i[1])/int(i[2])
               
                
                
                        explore.push((i[0],path+[(i[0],'yes')],cost+1+heuristic1,distance+int(i[1]),time+troad_normal,delivery_time+troad))
            return 'cant find path'

    #for finding shortest path
    def path_distance(start,end):
        explore=priority_queue()
        explore.push((start,[],0,0,0,0))# city,path,cost,distance,time,delivery time
        visited=[]
        def heuristic(city1,city2):
            R = 6373.0
            city11=city_dict[city1]
            city22=city_dict[city2]
            lon1,lat1=radians(float(city11[0])),radians(float(city11[1]))
            lon2,lat2=radians(float(city22[0])),radians(float(city22[1]))
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c
            return distance
        
        while explore.isempty()==False:
            node,path,cost,distance,time,delivery_time=explore.pop()
            visited.append(node)
        #print(path)
        #print(path,cost)
           # print(node,path,cost)
            if node==end:
                return len(path),path,distance,time,delivery_time
            
    #print(dict1[node])
    
            for i in dict1[node]:
               if i[0] not in visited:
                    if i[0] not in city_dict:
                    #print(i)
                        heuristic1=heuristic(start,end)-(distance+int(i[1]))
                        
                    else:
                        heuristic1=heuristic(i[0],end)
                    troad_normal=int(i[1])/int(i[2])
                    if int(i[2])>=50:
                            troad=int(i[1])/int(i[2])
                            p=tanh(int(i[1])/1000)
                            troad=troad+p*2*(time+troad)
                    else:
                            troad=int(i[1])/int(i[2])
               
                
                
                    explore.push((i[0],path+[(i[0],'yes')],cost+distance+heuristic1,distance+int(i[1]),time+troad_normal,delivery_time+troad))
        return 'cant find path'

    #for finding fastest route
    def fastpath(start,end):
        explore=priority_queue()
        explore.push((start,[],0,0,0,0))# city,path,cost,distance,time,delivery time
        visited=[]
        def heuristic(city1,city2):
            R = 6373.0
            city11=city_dict[city1]
            city22=city_dict[city2]
            lon1,lat1=float(city11[0]),float(city11[1])
            lon2,lat2=float(city22[0]),float(city22[1])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c
            return distance 
        
        while explore.isempty()==False:
            node,path,cost,distance,time,delivery_time=explore.pop()
            visited.append(node)
            #print(path)
        #print(path,cost)
        #print(node,path,cost)
            if node==end:
                return len(path),path,distance,time,delivery_time
            
    #print(dict1[node])
    
       
            for i in dict1[node]:
               if i[0] not in visited:
                    if i[0] not in city_dict:
                    #print(i)
                        heuristic1=(heuristic(start,end)-(distance+int(i[1])))/max_speed
                        
                    else:
                        heuristic1=heuristic(i[0],end)/int(i[1])
                    troad_normal=int(i[1])/int(i[2])
                    if int(i[2])>=50:
                            troad=int(i[1])/int(i[2])
                            p=tanh(int(i[1])/1000)
                            troad=troad+p*2*(time+troad)
                    else:
                            troad=int(i[1])/int(i[2])
               
                
                
                    explore.push((i[0],path+[(i[0],'yes')],cost+time+heuristic1,distance+int(i[1]),time+troad_normal,delivery_time+troad))
        return 'cant find path'
    #delivery time
    def fastpath_delivery(start,end):
        explore=priority_queue()
        explore.push((start,[],0,0,0,0))# city,path,cost,distance,time,delivery time
        visited=[]
        def heuristic(city1,city2):
            R = 6373.0
            city11=city_dict[city1]
            city22=city_dict[city2]
            lon1,lat1=float(city11[0]),float(city11[1])
            lon2,lat2=float(city22[0]),float(city22[1])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c
            return distance 
        
        while explore.isempty()==False:
            node,path,cost,distance,time,delivery_time=explore.pop()
            visited.append(node)
            #print(path)
        #print(path,cost)
        #print(node,path,cost)
            if node==end:
                return len(path),path,distance,time,delivery_time
            
    #print(dict1[node])
    
       
            for i in dict1[node]:
               if i[0] not in visited:
                    if i[0] not in city_dict:
                    #print(i)
                        heuristic1=(heuristic(start,end)-(distance+int(i[1])))/max_speed
                        
                    else:
                        heuristic1=heuristic(i[0],end)/int(i[1])
                    troad_normal=int(i[1])/int(i[2])
                    if int(i[2])>=50:
                            troad=int(i[1])/int(i[2])
                            p=tanh(int(i[1])/1000)
                            troad=troad+p*2*(time+troad)
                    else:
                            troad=int(i[1])/int(i[2])
               
                
                
                    explore.push((i[0],path+[(i[0],'yes')],cost+delivery_time+heuristic1,distance+int(i[1]),time+troad_normal,delivery_time+troad))
        return 'cant find path'

   
    
    
    if cost=='segments':
        a,route_taken,c,d,e=path_segments(start,end)
    if cost=='distance':
        a,route_taken,c,d,e=path_distance(start,end)
        #path_distance(start,end)
    if cost=='time':
        a,route_taken,c,d,e=fastpath(start,end)
    if cost=='delivery':
        a,route_taken,c,d,e=fastpath_delivery(start,end)
    

        

       


    

    #route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #               ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #               ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    return {"total-segments" : a, 
            "total-miles" : c, 
            "total-hours" : d, 
            "total-delivery-hours" : e, 
            "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)
    
    

    # Pretty print the route
    print("Start in %s" % start_city)
    
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])



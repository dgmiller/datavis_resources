"""
As of this writing, the lab computers do not have matplotlib's Basemap library
installed. If you want to install it, go to your terminal and type the command
'conda install basemap'. That should take care of everything. Then import the
library as shown below.
"""

from mpl_toolkits.basemap import Basemap

def get_data():
    """
    Gets water usage data for Los Angeles.
    We are most interested in latitude and longitude.
    The data is stored in a pandas dataframe.
    """
    web_address = "https://data.lacity.org/resource/v87k-wgde.json"
    df = pd.read_json(web_address)

    # the data is pretty messy
    # this code gets rid of everything we want
    df.drop(df.columns[:13],axis=1,inplace=True)
    J = json.loads(df['location_1'].to_json())
    df.drop(df.columns[-2:],axis=1,inplace=True)
    
    # the column of gps coordinates contains json data
    # this gets the gps coordinates from that column
    gps1 = []
    gps2 = []
    for j in range(len(J.keys())):
        gps1.append(J[str(j)]['coordinates'][0])
        gps2.append(J[str(j)]['coordinates'][1])
    # make longitude and latitude columns
    df['lon'] = gps1
    df['lat'] = gps2
    print df.head()
    return df

def plot_the_world(self,data,proj='merc'):
    """
    Shows some ways you can plot a map using Basemap. Consult Google and the 
    documentation for more details.
    IN
        data (pandas dataframe) a dataframe of the data to plot
        proj (string) the map projection to use, use 'robin' to plot the whole earth, default='merc'
    """
    # create a matplotlib Basemap object
    # that means create a map
    # I call it 'my_map' here
    if proj == 'robin':
        # this is a map of the world using the robinson projection
        # which is a pretty common projection
        # the center is at latitude = 0 and longitude = 0
        # experiment to see what the other keywords do
        my_map = Basemap(projection=proj,lat_0=0,lon_0=0,resolution='l',area_thresh=1000)
    else:
        # this is the mercator projection, which is a flat map
        # the latitude and longitude center this map around the united states
        # the other keywords help define the area you want to look at.
        my_map = Basemap(projection=proj,lat_0=33.,lon_0=-125.,resolution='l',area_thresh=1000.,
                llcrnrlon=-130.,llcrnrlat=25,urcrnrlon=-65., urcrnrlat=50)
    # now you have to draw stuff
    # it's pretty self-explanatory
    my_map.drawcoastlines(color='grey')
    my_map.drawcountries(color='grey')
    my_map.drawstates(color='grey')
    # this draws a color mask over the projection
    # you could put in details if you want
    # consult the documentation for details
    my_map.drawlsmask(land_color='white',ocean_color='white')
    my_map.drawmapboundary()
    # get the translated x,y coordinates of the map using lat and lon
    x,y = my_map(np.array(data['lon']),np.array(data['lat']))
    # scatter plot with constant bubble size
    my_map.plot(x,y,'ro',markersize=3,alpha=.4,linewidth=0)
    plt.show()
    
df = get_data()
plot_the_world(df)

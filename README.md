# Bing Map 

This [MLHub](https://mlhub.ai) package provides a demonstration and
command line tools built from Bing Map REST service provided through
Microsoft. This service can generate a list of coordinates (latitude
and longitude) based on the provided location. 

A Bing Map Key is required, allowing up to 50K geocodes a day, or 
150K total. Through
the [Bing Map Account](https://www.bingmapsportal.com/) create a Bing 
Map accont and use the key from the account for the *demo*. 


**Warning** Unlike the MLHub models in general these Bimg Map REST services
use *closed source services* which have no guarantee of ongoing
availability and do not come with the freedom to modify and share.

The Bing Map source code is available from
<https://github.com/JingjingShii/bing>.

## Quick Start

```console
$ ml geocode bing back creek
$ ml geocode bing back creek --max=1
$ ml geocode bing back creek --url
$ ml geocode bing back creek --bing
$ ml geocode bing back creek --google

```

## Usage

- To install mlhub (Ubuntu):

		$ pip3 install mlhub
		$ ml configure

- To install, configure, and run the demo:

		$ ml install   bing
		$ ml configure bing
		$ ml readme    bing
		$ ml commands  bing
		$ ml demo      bing
		
- Command line tools:

		$ ml geocode bing [options] <address>
		       -b            --bing               Generate Bing Maps URL.
			 -g            --google             Generate Google Maps URL.
			 -m <int>      --max=<int> 	    Maximum number of matches.
			 -o            --osm                Generate Open Street Map URL.
			 -u            --url                Generate Open Street Map URL.
			 -n            --neighborhood       Include the neighborhood when it is available.

## Command Line Tools

In addition to the *demo* command below, the package provides a number
of useful command line tools.

### *geocode*

The *geocode* command will generate a list of coordinate pairs for the provided
location. Each coordinate pair includes latitude and longitude. If the provided
location is specific, the result will be a list with one element. If the location
is ambiguous, such as a duplicate name in Australia, a list with several elements 
will be shown. It has the option to specify the maximum number of coordinates to 
return in the response. The number is between 1-20, and the default is 5. Also,
this service provides the option to include the neighborhood with the address
information when it is available. The default is 0 (Do not include neighborhood
information). We provide --google --bing and --osm option to show the location 
in the Google Map, Bing Map and Open street Map.

Not every location has neighborhood, the system will print available neighborhood if --inclnb 
is 1. 

```console
$ ml geocode bing PriceLine Pharmacy Albany Creek

$ ml geocode bing back creek --max=3
$ ml geocode bing back creek --inclnb

$ brave-browser `ml geocode bing --max=1 --osm albany creek`

$ brave-browser `ml geocode bing bunnings mentone 23-27 nepean hwy mentone vic 3194 --osm`

```

```console
$ ml geocode bing  Ballard, WA

47.669593811035156:-122.38619995117188,47.659759521484375:-122.39840698242188:47.67599868774414:-122.3759994506836,High,Ambiguous,Neighborhood,Ballard, WA, United States
47.675296783447266:-122.38217163085938,47.656524658203125:-122.4110336303711:47.697792053222656:-122.36068725585938,Medium,Ambiguous,Neighborhood,Ballard, WA, United States
```
For each line, the first element is coordinates, the second element is bounding
box, the thirdis confidence, fourth is match code, fifth is entity Type and the 
sixth is address.

## Demonstration
```console

=======
GEOCODE
=======

Here's an example. We provide the location

    Priceline Pharmacy Albany Creek

 and Bing will attempt to match this using its extensive map data. The
result includes the logitude, latitude, and neighbourhood bounding
box, how good the match is, the type of the location, and a clean
address.

Press Enter to continue: 

Latitude:  -27.35361099243164
Longitude: 152.96832275390625

Bounding Box: -27.372652053833008:152.94793701171875:-27.334684371948242:152.98854064941406

Confidence: Medium; Code: UpHierarchy

Type: PopulatedPlace

Address: Albany Creek, QLD, Australia

====
NEXT
====

You can use the 'geocode' command to obtain this output for yourself.

      $ ml geocode bing Priceline Pharmacy Albany Creek


```

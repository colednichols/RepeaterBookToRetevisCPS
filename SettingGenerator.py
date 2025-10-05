import csv
import os
import sys
import tkinter as tk
from tkinter import filedialog

# --- User-Definable Zone Configuration ---
# You can add or modify states and their county groupings here.
# Counties should be a single comma-separated string.
ZONE_DEFINITIONS = {
    "AL": {
        "Zone1": "Mobile,Baldwin,Escambia,Conecuh,Covington,Geneva,Houston,Dale,Henry,Coffee,Pike,Bullock,Macon,Russell,Barbour",
        "Zone2": "Washington,Choctaw,Clarke,Monroe,Butler,Crenshaw,Montgomery,Lowndes,Wilcox,Marengo,Sumter,Greene,Hale,Perry,Dallas,Autauga,Elmore",
        "Zone3": "Pickens,Tuscaloosa,Bibb,Chilton,Coosa,Tallapoosa,Chambers,Lee,Randolph,Clay,Talladega,Shelby,Jefferson,Walker,Fayette,Lamar",
        "Zone4": "Marion,Winston,Cullman,Blount,St. Clair,Calhoun,Cleburne,Cherokee,Etowah,Marshall,DeKalb,Jackson,Madison,Limestone,Morgan,Lawrence,Franklin,Colbert,Lauderdale"
    },
    "AK": {
        "Zone1": "Aleutians East,Aleutians West,Bristol Bay,Kodiak Island,Lake and Peninsula,Prince of Wales-Hyder,Ketchikan Gateway,Wrangell,Petersburg,Sitka,Juneau,Haines,Skagway,Yakutat,Hoonah-Angoon",
        "Zone2": "Kenai Peninsula,Anchorage,Matanuska-Susitna,Valdez-Cordova,Dillingham,Bethel",
        "Zone3": "Fairbanks North Star,Denali,Southeast Fairbanks,Yukon-Koyukuk,Copper River",
        "Zone4": "Nome,Northwest Arctic,North Slope,Kusilvak"
    },
    "AZ": {
        "Zone1": "Santa Cruz,Cochise,Pima,Yuma",
        "Zone2": "Pinal,Maricopa,Gila,La Paz",
        "Zone3": "Yavapai,Graham,Greenlee",
        "Zone4": "Mohave,Coconino,Navajo,Apache"
    },
    "AR": {
        "Zone1": "Miller,Lafayette,Columbia,Union,Ashley,Chicot,Hempstead,Nevada,Ouachita,Calhoun,Bradley,Drew,Little River,Sevier",
        "Zone2": "Howard,Pike,Clark,Hot Spring,Grant,Jefferson,Lincoln,Desha,Dallas,Cleveland,Saline,Pulaski,Lonoke,Arkansas,Garland,Montgomery",
        "Zone3": "Polk,Scott,Yell,Perry,Conway,Faulkner,White,Prairie,Monroe,Lee,Phillips,St. Francis,Woodruff,Jackson,Logan,Sebastian,Franklin,Johnson,Pope,Van Buren",
        "Zone4": "Crawford,Washington,Madison,Newton,Searcy,Stone,Izard,Sharp,Lawrence,Greene,Clay,Randolph,Fulton,Baxter,Marion,Boone,Carroll,Benton,Craighead,Mississippi,Poinsett,Cross,Crittenden,Independence,Cleburne"
    },
    "CA": {
        "Zone1": "San Diego,Imperial,Orange,Riverside",
        "Zone2": "Los Angeles,San Bernardino,Ventura,Santa Barbara,Kern",
        "Zone3": "San Luis Obispo,Monterey,Kings,Tulare,Fresno,Madera,Mariposa,Merced,Stanislaus,San Benito,Santa Cruz,Santa Clara,San Mateo",
        "Zone4": "Alameda,Contra Costa,San Francisco,Marin,Solano,Napa,Sonoma,Yolo,Sacramento,Placer,El Dorado,Amador,Calaveras,Tuolumne,Alpine,Mono,Inyo,San Joaquin,Sutter,Yuba,Nevada,Sierra,Plumas,Butte,Glenn,Colusa,Lake,Mendocino,Humboldt,Trinity,Tehama,Shasta,Lassen,Modoc,Siskiyou,Del Norte"
    },
    "CO": {
        "Zone1": "Baca,Las Animas,Huerfano,Costilla,Conejos,Rio Grande,Alamosa,Archuleta,La Plata,Montezuma",
        "Zone2": "Prowers,Bent,Otero,Pueblo,Custer,Saguache,Mineral,Hinsdale,San Juan,Dolores,San Miguel,Ouray,Montrose",
        "Zone3": "Kiowa,Cheyenne,Lincoln,Crowley,El Paso,Fremont,Chaffee,Gunnison,Delta,Mesa,Teller,Park,Lake,Pitkin,Eagle,Garfield",
        "Zone4": "Kit Carson,Yuma,Washington,Morgan,Adams,Arapahoe,Elbert,Douglas,Jefferson,Denver,Boulder,Weld,Larimer,Jackson,Routt,Moffat,Rio Blanco,Grand,Summit,Clear Creek,Gilpin,Broomfield,Logan,Sedgwick,Phillips"
    },
    "CT": {
        "Zone1": "Fairfield,New Haven",
        "Zone2": "Middlesex,New London",
        "Zone3": "Litchfield,Hartford",
        "Zone4": "Tolland,Windham"
    },
    "DE": {
        "Zone1": "Sussex",
        "Zone2": "Kent",
        "Zone3": "New Castle",
        "Zone4": "New Castle"
    },
    "DC": {
        "Zone1": "Ward 8,Ward 7",
        "Zone2": "Ward 6,Ward 5",
        "Zone3": "Ward 4,Ward 2",
        "Zone4": "Ward 3,Ward 1"
    },
    "FL": {
        "Zone1": "Monroe,Miami-Dade,Broward,Palm Beach,Collier,Hendry,Lee,Charlotte,Glades,Martin,St. Lucie,Okeechobee",
        "Zone2": "Sarasota,DeSoto,Hardee,Highlands,Indian River,Brevard,Osceola,Polk,Hillsborough,Manatee,Pinellas",
        "Zone3": "Pasco,Hernando,Citrus,Sumter,Lake,Orange,Seminole,Volusia,Marion,Flagler,Putnam,St. Johns,Alachua,Levy",
        "Zone4": "Dixie,Gilchrist,Union,Bradford,Clay,Duval,Nassau,Baker,Columbia,Suwannee,Hamilton,Madison,Taylor,Lafayette,Jefferson,Leon,Wakulla,Franklin,Gulf,Bay,Calhoun,Liberty,Gadsden,Jackson,Washington,Holmes,Walton,Okaloosa,Santa Rosa,Escambia"
    },
    "GA": {
        "Zone1": "Camden,Glynn,Brantley,Charlton,Ware,Clinch,Echols,Lanier,Lowndes,Brooks,Thomas,Grady,Decatur,Seminole,Miller,Early,Baker,Mitchell,Colquitt,Cook,Berrien,Atkinson,Coffee,Bacon,Pierce,Appling,Wayne,McIntosh",
        "Zone2": "Chatham,Bryan,Liberty,Long,Tattnall,Evans,Toombs,Jeff Davis,Ben Hill,Irwin,Tift,Worth,Turner,Crisp,Dooly,Wilcox,Telfair,Wheeler,Montgomery,Treutlen,Candler,Bulloch,Effingham,Screven,Jenkins,Burke,Emanuel,Johnson,Laurens,Dodge,Pulaski,Houston,Macon,Peach,Crawford,Bibb,Twiggs,Wilkinson",
        "Zone3": "Quitman,Clay,Calhoun,Dougherty,Lee,Terrell,Randolph,Stewart,Webster,Sumter,Schley,Marion,Chattahoochee,Muscogee,Harris,Talbot,Taylor,Upson,Monroe,Lamar,Pike,Spalding,Butts,Jasper,Jones,Putnam,Baldwin,Hancock,Washington,Glascock,Jefferson,Richmond,Columbia,McDuffie,Warren,Taliaferro,Greene,Morgan,Newton,Walton,Oconee,Clarke,Oglethorpe,Wilkes,Lincoln",
        "Zone4": "Heard,Troup,Meriwether,Coweta,Fayette,Henry,Rockdale,DeKalb,Fulton,Clayton,Douglas,Carroll,Haralson,Paulding,Cobb,Gwinnett,Barrow,Jackson,Madison,Elbert,Franklin,Hart,Stephens,Habersham,White,Lumpkin,Hall,Banks,Forsyth,Cherokee,Bartow,Polk,Floyd,Gordon,Pickens,Dawson,Union,Towns,Rabun,Fannin,Gilmer,Murray,Whitfield,Catoosa,Walker,Chattooga,Dade"
    },
    "HI": {
        "Zone1": "Hawaii",
        "Zone2": "Maui,Kalawao",
        "Zone3": "Honolulu",
        "Zone4": "Kauai"
    },
    "ID": {
        "Zone1": "Bear Lake,Franklin,Oneida,Cassia,Power,Bannock,Caribou,Bonneville,Teton,Madison,Fremont,Clark,Jefferson,Bingham",
        "Zone2": "Owyhee,Twin Falls,Jerome,Minidoka,Gooding,Lincoln,Blaine,Camas,Elmore,Butte,Custer,Lemhi",
        "Zone3": "Ada,Canyon,Gem,Payette,Washington,Adams,Valley,Boise",
        "Zone4": "Idaho,Lewis,Nez Perce,Clearwater,Latah,Benewah,Shoshone,Kootenai,Bonner,Boundary"
    },
    "IL": {
        "Zone1": "Alexander,Pulaski,Massac,Union,Johnson,Pope,Hardin,Jackson,Williamson,Saline,Gallatin,Franklin,Hamilton,White,Perry,Randolph,Monroe,St. Clair,Washington,Jefferson,Wayne,Edwards,Wabash",
        "Zone2": "Madison,Bond,Clinton,Marion,Clay,Richland,Lawrence,Fayette,Effingham,Jasper,Crawford,Montgomery,Macoupin,Jersey,Greene,Calhoun,Pike,Scott,Morgan,Sangamon,Christian,Shelby,Moultrie,Douglas,Coles,Cumberland,Clark,Edgar",
        "Zone3": "Adams,Brown,Cass,Menard,Logan,De Witt,Piatt,Champaign,Vermilion,Macon,Schuyler,Hancock,McDonough,Fulton,Mason,Tazewell,McLean,Ford,Iroquois,Peoria,Woodford,Livingston,Kankakee,Henderson,Warren,Knox,Stark,Marshall,Putnam,LaSalle,Grundy,Will",
        "Zone4": "Mercer,Rock Island,Henry,Bureau,Lee,DeKalb,Kane,DuPage,Cook,Kendall,Whiteside,Carroll,Ogle,Stephenson,Winnebago,Boone,McHenry,Lake,Jo Daviess"
    },
    "IN": {
        "Zone1": "Posey,Vanderburgh,Warrick,Spencer,Perry,Crawford,Harrison,Floyd,Clark,Jefferson,Switzerland,Ohio,Dearborn,Gibson,Pike,Dubois,Orange,Washington,Scott",
        "Zone2": "Knox,Daviess,Martin,Lawrence,Jackson,Jennings,Ripley,Franklin,Decatur,Bartholomew,Brown,Monroe,Greene,Sullivan,Vigo,Clay,Owen,Morgan,Johnson,Shelby,Rush,Fayette,Union",
        "Zone3": "Vermillion,Parke,Putnam,Hendricks,Marion,Hancock,Henry,Wayne,Randolph,Delaware,Madison,Hamilton,Boone,Montgomery,Fountain,Warren,Tippecanoe,Clinton,Tipton,Howard,Grant,Blackford,Jay",
        "Zone4": "Benton,White,Carroll,Cass,Miami,Wabash,Huntington,Wells,Adams,Allen,Whitley,Kosciusko,Fulton,Pulaski,Jasper,Newton,Lake,Porter,LaPorte,St. Joseph,Marshall,Starke,Elkhart,Lagrange,Steuben,DeKalb,Noble"
    },
    "IA": {
        "Zone1": "Fremont,Page,Taylor,Ringgold,Decatur,Wayne,Appanoose,Davis,Van Buren,Lee,Mills,Montgomery,Adams,Union,Clarke,Lucas,Monroe,Wapello,Jefferson,Henry,Des Moines",
        "Zone2": "Pottawattamie,Cass,Adair,Madison,Warren,Marion,Mahaska,Keokuk,Washington,Louisa,Muscatine,Scott,Cedar,Clinton,Jackson",
        "Zone3": "Harrison,Shelby,Audubon,Guthrie,Dallas,Polk,Jasper,Poweshiek,Iowa,Johnson,Jones,Monona,Crawford,Carroll,Greene,Boone,Story,Marshall,Tama,Benton,Linn",
        "Zone4": "Woodbury,Ida,Sac,Calhoun,Webster,Hamilton,Hardin,Grundy,Black Hawk,Buchanan,Delaware,Dubuque,Plymouth,Cherokee,Buena Vista,Pocahontas,Humboldt,Wright,Franklin,Butler,Bremer,Fayette,Clayton,Sioux,O'Brien,Clay,Palo Alto,Hancock,Cerro Gordo,Floyd,Chickasaw,Winneshiek,Allamakee,Lyon,Osceola,Dickinson,Emmet,Kossuth,Winnebago,Worth,Mitchell,Howard"
    },
    "KS": {
        "Zone1": "Morton,Stevens,Seward,Meade,Clark,Comanche,Barber,Harper,Sumner,Cowley,Chautauqua,Montgomery,Labette,Cherokee",
        "Zone2": "Greeley,Wichita,Scott,Lane,Ness,Rush,Barton,Rice,McPherson,Marion,Chase,Lyon,Coffey,Anderson,Linn,Bourbon,Crawford,Stanton,Grant,Haskell,Gray,Ford,Kiowa,Pratt,Kingman,Sedgwick,Butler,Greenwood,Woodson,Allen,Neosho,Wilson",
        "Zone3": "Hamilton,Kearny,Finney,Hodgeman,Pawnee,Stafford,Reno,Harvey,Saline,Dickinson,Morris,Wabaunsee,Shawnee,Osage,Franklin,Miami,Johnson,Wyandotte,Leavenworth,Douglas,Geary",
        "Zone4": "Wallace,Logan,Gove,Trego,Ellis,Russell,Lincoln,Ellsworth,Ottawa,Cloud,Clay,Riley,Pottawatomie,Jackson,Atchison,Doniphan,Brown,Nemaha,Marshall,Washington,Republic,Jewell,Mitchell,Osborne,Rooks,Graham,Sheridan,Thomas,Sherman,Cheyenne,Rawlins,Decatur,Norton,Phillips,Smith"
    },
    "KY": {
        "Zone1": "Fulton,Hickman,Carlisle,Ballard,McCracken,Graves,Calloway,Marshall,Livingston,Lyon,Trigg,Christian,Todd,Logan,Simpson,Allen,Monroe,Cumberland,Clinton,Wayne,McCreary,Whitley,Bell",
        "Zone2": "Crittenden,Union,Webster,Hopkins,Muhlenberg,Butler,Warren,Barren,Metcalfe,Adair,Russell,Pulaski,Laurel,Knox,Harlan,Letcher,Pike",
        "Zone3": "Henderson,Daviess,McLean,Ohio,Grayson,Hardin,LaRue,Hart,Green,Taylor,Casey,Lincoln,Rockcastle,Jackson,Owsley,Clay,Leslie,Perry,Knott,Floyd",
        "Zone4": "Hancock,Breckinridge,Meade,Bullitt,Nelson,Washington,Marion,Boyle,Garrard,Madison,Estill,Lee,Wolfe,Breathitt,Magoffin,Johnson,Martin,Lawrence,Boyd,Greenup,Carter,Elliott,Morgan,Menifee,Powell,Clark,Fayette,Jessamine,Mercer,Anderson,Spencer,Jefferson,Oldham,Trimble,Henry,Shelby,Franklin,Scott,Woodford,Bourbon,Nicholas,Bath,Rowan,Montgomery,Fleming,Mason,Robertson,Bracken,Pendleton,Grant,Owen,Gallatin,Carroll,Boone,Kenton,Campbell,Harrison"
    },
    "LA": {
        "Zone1": "Cameron,Vermilion,Iberia,St. Mary,Terrebonne,Lafourche,Plaquemines,St. Bernard,Jefferson",
        "Zone2": "Calcasieu,Jefferson Davis,Acadia,Lafayette,St. Martin,Assumption,St. James,St. John the Baptist,St. Charles,Orleans,St. Tammany,Washington,Tangipahoa",
        "Zone3": "Beauregard,Allen,Evangeline,St. Landry,Pointe Coupee,Iberville,Ascension,Livingston,St. Helena,East Baton Rouge,West Baton Rouge,West Feliciana,East Feliciana",
        "Zone4": "Vernon,Sabine,De Soto,Caddo,Bossier,Webster,Claiborne,Union,Morehouse,West Carroll,East Carroll,Madison,Richland,Ouachita,Lincoln,Jackson,Bienville,Red River,Natchitoches,Winn,Grant,La Salle,Catahoula,Concordia,Tensas,Franklin,Caldwell,Rapides,Avoyelles"
    },
    "ME": {
        "Zone1": "York,Cumberland",
        "Zone2": "Sagadahoc,Androscoggin,Kennebec,Lincoln,Knox,Waldo",
        "Zone3": "Oxford,Franklin,Somerset,Piscataquis,Hancock,Penobscot,Washington",
        "Zone4": "Aroostook"
    },
    "MD": {
        "Zone1": "Worcester,Somerset,Wicomico,Dorchester,Talbot,Queen Anne's,Caroline,Kent",
        "Zone2": "St. Mary's,Calvert,Charles,Prince George's,Anne Arundel",
        "Zone3": "Montgomery,Howard,Baltimore,Baltimore City,Harford,Cecil",
        "Zone4": "Frederick,Washington,Allegany,Garrett,Carroll"
    },
    "MA": {
        "Zone1": "Barnstable,Dukes,Nantucket,Plymouth,Bristol",
        "Zone2": "Norfolk,Suffolk,Middlesex,Essex",
        "Zone3": "Worcester,Hampden,Hampshire",
        "Zone4": "Franklin,Berkshire"
    },
    "MI": {
        "Zone1": "Monroe,Lenawee,Hillsdale,Branch,St. Joseph,Cass,Berrien,Van Buren,Kalamazoo,Calhoun,Jackson,Washtenaw,Wayne",
        "Zone2": "Allegan,Barry,Eaton,Ingham,Livingston,Oakland,Macomb,St. Clair,Lapeer,Genesee,Shiawassee,Clinton,Ionia,Kent,Ottawa,Muskegon",
        "Zone3": "Montcalm,Gratiot,Saginaw,Tuscola,Huron,Sanilac,Isabella,Midland,Bay,Gladwin,Arenac,Iosco,Ogemaw,Roscommon,Clare,Mecosta,Newaygo,Oceana,Mason,Lake,Osceola",
        "Zone4": "Manistee,Wexford,Missaukee,Crawford,Oscoda,Alcona,Alpena,Presque Isle,Montmorency,Otsego,Antrim,Kalkaska,Grand Traverse,Leelanau,Benzie,Emmet,Cheboygan,Charlevoix,Luce,Chippewa,Mackinac,Schoolcraft,Alger,Delta,Menominee,Dickinson,Marquette,Iron,Baraga,Houghton,Keweenaw,Ontonagon,Gogebic"
    },
    "MN": {
        "Zone1": "Houston,Fillmore,Mower,Freeborn,Faribault,Martin,Jackson,Nobles,Rock,Pipestone,Murray,Cottonwood,Watonwan,Blue Earth,Waseca,Steele,Dodge,Olmsted,Winona",
        "Zone2": "Lincoln,Lyon,Redwood,Brown,Nicollet,Le Sueur,Rice,Goodhue,Wabasha,Yellow Medicine,Renville,Sibley,Scott,Dakota,Washington,Ramsey,Hennepin,Carver,McLeod",
        "Zone3": "Lac qui Parle,Chippewa,Kandiyohi,Meeker,Wright,Anoka,Chisago,Isanti,Sherburne,Stearns,Pope,Swift,Big Stone,Traverse,Stevens,Grant,Douglas,Todd,Morrison,Mile Lacs,Kanabec,Pine,Benton",
        "Zone4": "Wilkin,Otter Tail,Wadena,Cass,Crow Wing,Aitkin,Carlton,St. Louis,Lake,Cook,Itasca,Koochiching,Beltrami,Hubbard,Clearwater,Mahnomen,Becker,Clay,Norman,Polk,Red Lake,Pennington,Marshall,Kittson,Roseau,Lake of the Woods"
    },
    "MS": {
        "Zone1": "Hancock,Harrison,Jackson,Pearl River,Stone,George,Forrest,Lamar,Marion,Walthall,Pike,Amite,Wilkinson",
        "Zone2": "Adams,Franklin,Lincoln,Lawrence,Jefferson Davis,Covington,Jones,Wayne,Greene,Perry,Copiah,Simpson,Smith,Jasper,Clarke",
        "Zone3": "Claiborne,Jefferson,Hinds,Rankin,Scott,Newton,Lauderdale,Warren,Issaquena,Sharkey,Yazoo,Madison,Leake,Neshoba,Kemper",
        "Zone4": "Washington,Humphreys,Holmes,Attala,Winston,Noxubee,Lowndes,Oktibbeha,Choctaw,Webster,Montgomery,Carroll,Leflore,Sunflower,Bolivar,Coahoma,Quitman,Tallahatchie,Grenada,Yalobusha,Calhoun,Chickasaw,Monroe,Clay,Panola,Lafayette,Pontotoc,Lee,Itawamba,Union,Tippah,Alcorn,Tishomingo,Prentiss,Benton,Marshall,DeSoto,Tate,Tunica"
    },
    "MO": {
        "Zone1": "Dunklin,Pemiscot,New Madrid,Mississippi,Scott,Stoddard,Butler,Ripley,Oregon,Shannon,Carter,Wayne,Bollinger,Cape Girardeau,Perry,Ste. Genevieve,St. Francois,Madison,Iron,Reynolds,Dent,Texas,Howell,Ozark",
        "Zone2": "Barry,Stone,Taney,Douglas,Wright,Laclede,Pulaski,Phelps,Crawford,Washington,Jefferson,St. Louis,St. Louis City,Franklin,Gasconade,Maries,Camden,Hickory,Polk,Greene,Christian,Lawrence,McDonald,Newton,Jasper",
        "Zone3": "Barton,Vernon,St. Clair,Benton,Morgan,Moniteau,Cole,Osage,Miller,Pettis,Henry,Bates,Cass,Jackson,Lafayette,Saline,Howard,Boone,Callaway,Montgomery,Warren,St. Charles,Lincoln,Pike,Ralls,Audrain",
        "Zone4": "Dade,Cedar,Johnson,Cooper,Randolph,Monroe,Shelby,Marion,Lewis,Clark,Scotland,Knox,Adair,Macon,Chariton,Linn,Sullivan,Putnam,Schuyler,Mercer,Grundy,Livingston,Daviess,Harrison,Worth,Gentry,Nodaway,Atchison,Holt,Andrew,DeKalb,Caldwell,Ray,Carroll,Buchanan,Clinton,Platte,Clay"
    },
    "MT": {
        "Zone1": "Carter,Powder River,Fallon,Custer,Prairie,Dawson,Wibaux,Rosebud,Garfield,McCone,Richland,Valley,Daniels,Sheridan,Roosevelt",
        "Zone2": "Big Horn,Yellowstone,Treasure,Musselshell,Golden Valley,Wheatland,Sweet Grass,Stillwater,Carbon,Park,Gallatin,Meagher,Judith Basin,Fergus,Petroleum",
        "Zone3": "Beaverhead,Madison,Jefferson,Silver Bow,Deer Lodge,Granite,Powell,Lewis and Clark,Broadwater,Cascade,Teton,Pondera,Toole,Liberty,Hill,Blaine,Phillips,Chouteau",
        "Zone4": "Ravalli,Missoula,Lake,Flathead,Lincoln,Sanders,Mineral"
    },
    "NE": {
        "Zone1": "Richardson,Pawnee,Gage,Jefferson,Thayer,Nuckolls,Webster,Franklin,Harlan,Furnas,Red Willow,Hitchcock,Dundy",
        "Zone2": "Nemaha,Otoe,Johnson,Lancaster,Saline,Fillmore,Clay,Adams,Kearney,Phelps,Gosper,Frontier,Hayes,Chase,Perkins",
        "Zone3": "Cass,Sarpy,Douglas,Washington,Burt,Thurston,Dakota,Dixon,Cedar,Knox,Boyd,Holt,Garfield,Wheeler,Boone,Platte,Colfax,Dodge,Saunders,Butler,Seward,York,Hamilton,Merrick,Nance,Greeley,Valley,Custer,Dawson,Buffalo,Hall,Howard,Sherman",
        "Zone4": "Antelope,Pierce,Wayne,Madison,Stanton,Cuming,Rock,Brown,Keya Paha,Cherry,Sheridan,Dawes,Sioux,Box Butte,Scotts Bluff,Banner,Kimball,Cheyenne,Deuel,Garden,Morrill,Grant,Hooker,Thomas,Blaine,Loup,Arthur,McPherson,Logan,Lincoln,Keith"
    },
    "NV": {
        "Zone1": "Clark,Lincoln",
        "Zone2": "Nye,Esmeralda,Mineral",
        "Zone3": "Lyon,Douglas,Carson City,Storey,Washoe,Churchill,Pershing,Lander,Eureka",
        "Zone4": "Humboldt,Elko,White Pine"
    },
    "NH": {
        "Zone1": "Rockingham,Hillsborough,Cheshire",
        "Zone2": "Strafford,Merrimack,Sullivan",
        "Zone3": "Belknap,Carroll,Grafton",
        "Zone4": "Coos"
    },
    "NJ": {
        "Zone1": "Cape May,Cumberland,Salem,Gloucester,Camden,Atlantic,Burlington,Ocean",
        "Zone2": "Monmouth,Middlesex,Mercer,Hunterdon,Somerset",
        "Zone3": "Union,Essex,Hudson,Warren,Morris",
        "Zone4": "Passaic,Bergen,Sussex"
    },
    "NM": {
        "Zone1": "Doña Ana,Luna,Hidalgo,Otero",
        "Zone2": "Lincoln,Chaves,Eddy,Lea,Sierra,Grant,Catron",
        "Zone3": "Torrance,Socorro,Valencia,Bernalillo,Santa Fe,Guadalupe,De Baca,Roosevelt,Curry,Quay",
        "Zone4": "San Juan,McKinley,Rio Arriba,Taos,Colfax,Union,Mora,Harding,San Miguel,Sandoval,Los Alamos,Cibola"
    },
    "NY": {
        "Zone1": "Suffolk,Nassau,Queens,Kings,Richmond,New York,Bronx,Westchester,Rockland",
        "Zone2": "Putnam,Orange,Dutchess,Ulster,Sullivan,Greene,Columbia,Albany,Rensselaer,Schenectady,Saratoga,Washington",
        "Zone3": "Schoharie,Delaware,Otsego,Chenango,Broome,Tioga,Tompkins,Chemung,Schuyler,Steuben,Yates,Seneca,Cayuga,Onondaga,Cortland,Madison,Oneida,Herkimer,Montgomery,Fulton,Hamilton,Warren,Essex",
        "Zone4": "Oswego,Lewis,Jefferson,St. Lawrence,Franklin,Clinton,Onondaga,Wayne,Ontario,Livingston,Monroe,Orleans,Genesee,Wyoming,Allegany,Cattaraugus,Chautauqua,Erie,Niagara"
    },
    "NC": {
        "Zone1": "Brunswick,New Hanover,Pender,Onslow,Carteret,Pamlico,Beaufort,Hyde,Dare,Tyrrell,Washington,Bertie,Hertford,Gates,Chowan,Perquimans,Pasquotank,Camden,Currituck,Martin,Pitt,Craven,Jones,Lenoir,Greene,Wayne,Duplin,Sampson,Bladen,Columbus,Robeson,Scotland,Hoke,Cumberland",
        "Zone2": "Richmond,Moore,Lee,Harnett,Johnston,Wilson,Edgecombe,Nash,Franklin,Wake,Chatham,Randolph,Montgomery,Anson,Union,Mecklenburg,Cabarrus,Stanly,Rowan,Davidson,Guilford,Alamance,Orange,Durham,Person,Granville,Vance,Warren,Halifax,Northampton",
        "Zone3": "Caswell,Rockingham,Stokes,Surry,Yadkin,Forsyth,Davie,Iredell,Lincoln,Gaston,Cleveland,Rutherford,Polk,Henderson,Transylvania",
        "Zone4": "Buncombe,McDowell,Burke,Catawba,Alexander,Wilkes,Alleghany,Ashe,Watauga,Avery,Mitchell,Yancey,Madison,Haywood,Swain,Jackson,Macon,Clay,Cherokee,Graham"
    },
    "ND": {
        "Zone1": "Richland,Sargent,Ransom,Dickey,LaMoure,McIntosh,Logan,Emmons",
        "Zone2": "Cass,Traill,Steele,Griggs,Barnes,Stutsman,Kidder,Burleigh,Sioux,Grant,Morton",
        "Zone3": "Grand Forks,Walsh,Nelson,Eddy,Foster,Wells,Sheridan,McLean,Oliver,Mercer,Dunn,Billings,Stark,Hettinger,Adams,Bowman,Slope,Golden Valley",
        "Zone4": "Pembina,Cavalier,Towner,Ramsey,Benson,Pierce,Rolette,McHenry,Bottineau,Ward,Renville,Burke,Mountrail,Williams,McKenzie,Divide"
    },
    "OH": {
        "Zone1": "Hamilton,Clermont,Brown,Adams,Scioto,Lawrence,Gallia,Meigs,Athens,Vinton,Jackson,Pike,Highland,Clinton,Warren,Butler",
        "Zone2": "Preble,Montgomery,Greene,Fayette,Ross,Hocking,Perry,Morgan,Washington,Noble,Monroe,Belmont,Jefferson,Guernsey,Muskingum,Licking,Fairfield,Pickaway,Madison,Clark,Champaign,Miami",
        "Zone3": "Darke,Shelby,Logan,Union,Delaware,Franklin,Knox,Coshocton,Tuscarawas,Harrison,Carroll,Stark,Wayne,Holmes,Ashland,Richland,Morrow,Marion,Hardin,Auglaize,Mercer",
        "Zone4": "Van Wert,Allen,Hancock,Wyandot,Crawford,Seneca,Sandusky,Ottawa,Erie,Huron,Lorain,Cuyahoga,Medina,Summit,Portage,Mahoning,Columbiana,Trumbull,Geauga,Ashtabula,Lake,Lucas,Wood,Henry,Defiance,Paulding,Putnam,Williams,Fulton"
    },
    "OK": {
        "Zone1": "McCurtain,Choctaw,Bryan,Marshall,Love,Jefferson,Cotton,Tillman,Jackson,Harmon,Greer,Kiowa,Comanche,Stephens,Carter,Johnston,Atoka,Pushmataha",
        "Zone2": "Le Flore,Latimer,Pittsburg,Coal,Pontotoc,Murray,Garvin,McClain,Cleveland,Pottawatomie,Seminole,Hughes,Haskell,Sequoyah,Adair,Cherokee",
        "Zone3": "Beckham,Roger Mills,Custer,Washita,Caddo,Grady,Canadian,Oklahoma,Lincoln,Okfuskee,Okmulgee,Muskogee,Wagoner,McIntosh,Creek,Payne,Logan,Kingfisher,Blaine,Dewey,Ellis",
        "Zone4": "Beaver,Texas,Cimarron,Harper,Woods,Alfalfa,Grant,Kay,Osage,Washington,Nowata,Craig,Ottawa,Delaware,Mayes,Rogers,Tulsa,Pawnee,Noble,Garfield,Major,Woodward"
    },
    "OR": {
        "Zone1": "Curry,Josephine,Jackson,Klamath,Lake,Harney,Malheur",
        "Zone2": "Coos,Douglas,Lane,Linn,Benton,Lincoln,Deschutes,Crook,Grant",
        "Zone3": "Tillamook,Polk,Marion,Clackamas,Multnomah,Washington,Yamhill,Jefferson,Wheeler,Wasco",
        "Zone4": "Hood River,Sherman,Gilliam,Morrow,Umatilla,Union,Wallowa,Baker,Columbia,Clatsop"
    },
    "PA": {
        "Zone1": "Philadelphia,Delaware,Chester,Lancaster,York,Adams,Franklin,Fulton,Bedford,Somerset,Fayette,Greene,Washington",
        "Zone2": "Bucks,Montgomery,Berks,Lebanon,Dauphin,Cumberland,Perry,Juniata,Mifflin,Huntingdon,Blair,Cambria,Westmoreland,Allegheny",
        "Zone3": "Northampton,Lehigh,Schuylkill,Carbon,Monroe,Pike,Wayne,Lackawanna,Luzerne,Columbia,Montour,Northumberland,Snyder,Union,Lycoming,Clinton,Centre,Clearfield,Indiana,Armstrong,Beaver,Butler,Lawrence",
        "Zone4": "Susquehanna,Bradford,Tioga,Potter,McKean,Warren,Erie,Crawford,Mercer,Venango,Forest,Elk,Cameron,Clarion,Jefferson"
    },
    "RI": {
        "Zone1": "Washington,Newport",
        "Zone2": "Kent",
        "Zone3": "Bristol,Providence",
        "Zone4": "Providence"
    },
    "SC": {
        "Zone1": "Beaufort,Jasper,Hampton,Colleton,Charleston,Dorchester,Berkeley,Georgetown,Horry",
        "Zone2": "Allendale,Barnwell,Bamberg,Orangeburg,Calhoun,Clarendon,Williamsburg,Sumter,Lee,Darlington,Florence,Marion,Dillon,Marlboro",
        "Zone3": "Aiken,Edgefield,McCormick,Saluda,Lexington,Richland,Kershaw,Chesterfield,Lancaster,Fairfield,Newberry",
        "Zone4": "Abbeville,Greenwood,Laurens,Union,York,Chester,Greenville,Anderson,Spartanburg,Cherokee,Oconee,Pickens"
    },
    "SD": {
        "Zone1": "Union,Clay,Yankton,Bon Homme,Charles Mix,Gregory,Tripp,Todd,Bennett,Oglala Lakota,Fall River,Custer",
        "Zone2": "Lincoln,Turner,Hutchinson,Douglas,Brule,Lyman,Jones,Jackson,Pennington,Lawrence,Meade",
        "Zone3": "Minnehaha,McCook,Hanson,Davison,Aurora,Jerauld,Sanborn,Miner,Lake,Moody,Buffalo,Hand,Hyde,Hughes,Sully,Potter,Stanley,Haakon,Ziebach,Dewey,Corson,Perkins",
        "Zone4": "Brookings,Kingsbury,Beadle,Spink,Faulk,Edmunds,McPherson,Brown,Marshall,Day,Grant,Codington,Hamlin,Deuel,Clark,Roberts,Campbell,Walworth"
    },
    "TN": {
        "Zone1": "Shelby,Fayette,Hardeman,McNairy,Hardin,Wayne,Lawrence,Giles,Lincoln,Franklin,Marion,Hamilton,Bradley,Polk",
        "Zone2": "Tipton,Haywood,Madison,Chester,Henderson,Decatur,Perry,Lewis,Maury,Marshall,Bedford,Coffee,Moore,Grundy,Sequatchie,Bledsoe,Rhea,Meigs,McMinn",
        "Zone3": "Lauderdale,Dyer,Crockett,Gibson,Carroll,Benton,Humphreys,Hickman,Williamson,Rutherford,Cannon,Warren,Van Buren,White,Cumberland,Roane,Loudon,Monroe",
        "Zone4": "Obion,Weakley,Henry,Stewart,Houston,Montgomery,Dickson,Cheatham,Robertson,Davidson,Wilson,Sumner,Trousdale,Macon,Smith,DeKalb,Putnam,Overton,Fentress,Pickett,Clay,Jackson,Scott,Morgan,Anderson,Knox,Blount,Sevier,Cocke,Greene,Washington,Unicoi,Carter,Johnson,Sullivan,Hawkins,Hamblen,Grainger,Union,Claiborne,Campbell,Hancock,Jefferson"
    },
    "TX": {
        "Zone1": "Cameron,Hidalgo,Starr,Zapata,Webb,Maverick,Dimmit,La Salle,Frio,Zavala,Uvalde,Medina,Bexar,Atascosa,McMullen,Live Oak,Jim Wells,Kleberg,Kenedy,Willacy,Brooks,Duval,Jim Hogg,Kinney,Val Verde,Terrell,Brewster,Presidio,Jeff Davis,Culberson,Hudspeth,El Paso",
        "Zone2": "Nueces,San Patricio,Aransas,Refugio,Calhoun,Victoria,Goliad,Bee,Karnes,Wilson,Guadalupe,Gonzales,DeWitt,Lavaca,Jackson,Matagorda,Wharton,Fort Bend,Brazoria,Galveston,Harris,Chambers,Jefferson,Orange,Hardin,Liberty,Montgomery,Walker,San Jacinto,Polk,Tyler,Jasper,Newton,Sabine,San Augustine,Angelina,Nacogdoches,Shelby,Panola,Rusk,Cherokee,Houston,Trinity,Leon,Madison,Grimes,Waller,Austin,Colorado,Fayette,Lee,Burleson,Washington,Brazos",
        "Zone3": "Bastrop,Travis,Williamson,Milam,Robertson,Falls,Limestone,Freestone,Anderson,Henderson,Navarro,Ellis,Dallas,Tarrant,Johnson,Hill,Bosque,Somervell,Hood,Erath,Comanche,Hamilton,Mills,Coryell,McLennan,Bell,Lampasas,Burnet,Llano,Blanco,Hays,Caldwell,Comal,Kendall,Gillespie,Mason,McCulloch,San Saba,Brown,Coleman,Runnels,Concho,Tom Green,Irion,Schleicher,Sutton,Edwards,Real,Bandera,Kerr,Kimble,Menard,Crockett,Reagan,Upton,Crane,Pecos,Reeves,Ward,Winkler,Ector,Midland,Glasscock,Sterling,Coke,Taylor,Callahan,Eastland,Stephens,Palo Pinto,Parker,Wise,Denton,Collin,Rockwall,Kaufman,Van Zandt,Wood,Upshur,Gregg,Smith,Harrison,Marion,Cass,Morris,Titus,Camp,Franklin,Hopkins,Rains,Hunt,Delta,Lamar,Fannin,Grayson,Cooke,Montague,Jack,Young,Throckmorton,Shackelford,Jones,Fisher,Nolan,Mitchell,Howard,Martin,Andrews,Gaines,Dawson,Borden,Scurry,Stonewall,Haskell,Knox,Baylor,Archer,Clay,Wichita",
        "Zone4": "Foard,Hardeman,Wilbarger,King,Cottle,Motley,Dickens,Garza,Kent,Lynn,Terry,Yoakum,Cochran,Hockley,Lubbock,Crosby,Floyd,Hale,Lamb,Bailey,Parmer,Castro,Swisher,Briscoe,Hall,Childress,Collingsworth,Donley,Armstrong,Randall,Deaf Smith,Oldham,Potter,Carson,Gray,Wheeler,Hemphill,Roberts,Ochiltree,Lipscomb,Hansford,Sherman,Moore,Hutchinson,Dallam,Hartley"
    },
    "UT": {
        "Zone1": "Washington,Kane,Garfield,Iron,Beaver",
        "Zone2": "Piute,Wayne,Sevier,Sanpete,Millard,Juab,Emery,Grand,San Juan",
        "Zone3": "Utah,Wasatch,Duchesne,Uintah,Carbon,Tooele",
        "Zone4": "Salt Lake,Davis,Morgan,Weber,Rich,Cache,Box Elder,Summit,Daggett"
    },
    "VT": {
        "Zone1": "Bennington,Windham",
        "Zone2": "Rutland,Windsor",
        "Zone3": "Addison,Orange,Washington,Chittenden",
        "Zone4": "Lamoille,Caledonia,Essex,Orleans,Franklin,Grand Isle"
    },
    "VA": {
        "Zone1": "Lee,Scott,Wise,Dickenson,Buchanan,Russell,Washington,Smyth,Grayson,Tazewell,Bland,Wythe,Carroll,Pulaski,Giles,Montgomery,Floyd,Patrick,Henry,Franklin,Roanoke,Craig,Botetourt",

        "Zone2": "Alleghany,Bath,Highland,Augusta,Rockbridge,Nelson,Amherst,Bedford,Campbell,Appomattox,Buckingham,Cumberland,Prince Edward,Charlotte,Halifax,Mecklenburg,Brunswick,Lunenburg,Nottoway,Amelia,Powhatan,Chesterfield,Dinwiddie,Greensville,Sussex,Southampton,Isle of Wight,Surry,Prince George,Hopewell,Petersburg,Colonial Heights,Richmond City,Henrico,Hanover",
        "Zone3": "Goochland,Louisa,Fluvanna,Albemarle,Greene,Madison,Orange,Spotsylvania,Caroline,King George,Westmoreland,Northumberland,Lancaster,Richmond County,Essex,King and Queen,King William,New Kent,Charles City,James City,York,Gloucester,Mathews,Middlesex,Accomack,Northampton,Virginia Beach,Norfolk,Portsmouth,Chesapeake,Suffolk,Hampton,Newport News,Poquoson,Williamsburg",
        "Zone4": "Fauquier,Rappahannock,Culpeper,Stafford,Prince William,Fairfax,Loudoun,Arlington,Clarke,Frederick,Warren,Shenandoah,Page,Rockingham,Alexandria,Fairfax City,Falls Church,Manassas,Manassas Park"
    },
    "WA": {
        "Zone1": "Clark,Skamania,Klickitat,Wahkiakum,Cowlitz,Lewis,Pacific",
        "Zone2": "Thurston,Pierce,King,Kitsap,Mason,Grays Harbor,Jefferson,Clallam",
        "Zone3": "Whatcom,Skagit,Snohomish,Island,San Juan,Kittitas,Yakima,Benton,Franklin,Walla Walla,Columbia,Garfield,Asotin",
        "Zone4": "Okanogan,Chelan,Douglas,Grant,Adams,Whitman,Spokane,Lincoln,Ferry,Stevens,Pend Oreille"
    },
    "WV": {
        "Zone1": "McDowell,Wyoming,Mercer,Raleigh,Fayette,Summers,Monroe,Greenbrier",
        "Zone2": "Mingo,Logan,Boone,Kanawha,Nicholas,Pocahontas,Webster,Clay",
        "Zone3": "Wayne,Cabell,Putnam,Lincoln,Mason,Jackson,Roane,Calhoun,Gilmer,Braxton,Lewis,Upshur,Randolph,Pendleton",
        "Zone4": "Wood,Wirt,Ritchie,Doddridge,Harrison,Barbour,Tucker,Grant,Hardy,Hampshire,Mineral,Morgan,Berkeley,Jefferson,Pleasants,Tyler,Wetzel,Marion,Monongalia,Preston,Taylor,Marshall,Ohio,Brooke,Hancock"
    },
    "WI": {
        "Zone1": "Kenosha,Racine,Walworth,Rock,Green,Lafayette,Grant,Crawford,Vernon",
        "Zone2": "Milwaukee,Waukesha,Jefferson,Dane,Iowa,Sauk,Richland,Columbia,Dodge,Washington,Ozaukee",
        "Zone3": "Sheboygan,Fond du Lac,Green Lake,Marquette,Adams,Juneau,Monroe,La Crosse,Jackson,Trempealeau,Buffalo,Pepin,Eau Claire,Clark,Wood,Portage,Waushara,Winnebago,Calumet,Manitowoc,Kewaunee,Door,Brown,Outagamie,Waupaca",
        "Zone4": "Oconto,Menominee,Shawano,Marathon,Taylor,Chippewa,Dunn,Pierce,St. Croix,Polk,Barron,Rusk,Lincoln,Langlade,Forest,Florence,Marinette,Oneida,Vilas,Price,Sawyer,Ashland,Iron,Burnett,Washburn,Douglas,Bayfield"
    },
    "WY": {
        "Zone1": "Laramie,Albany,Carbon,Sweetwater,Uinta",
        "Zone2": "Platte,Goshen,Niobrara,Converse,Natrona",
        "Zone3": "Fremont,Sublette,Lincoln,Teton,Hot Springs",
        "Zone4": "Washakie,Big Horn,Park,Sheridan,Johnson,Campbell,Crook,Weston"
    }
}


ZONE_CHANNEL_LIMIT = 64

# --- User-Definable Filter Configuration ---
ENABLE_FREQUENCY_FILTER = True  # Set to False to disable this filter
VHF_RANGE = [136.0, 174.0]  # Min and Max for VHF band in MHz
UHF_RANGE = [400.0, 480.0]  # Min and Max for UHF band in MHz


def get_hardcoded_gmrs_channels():
    """Returns a hardcoded list of VFO and GMRS channels."""
    return [
        {'No.': 'VFOA', 'Alias': 'VFO-A', 'Rx Freq[MHz]': '147.42', 'Tx Freq[MHz]': '147.42', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 'VFOB', 'Alias': 'VFO-B', 'Rx Freq[MHz]': '445', 'Tx Freq[MHz]': '445', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 1, 'Alias': 'GMRS-01', 'Rx Freq[MHz]': '462.5625', 'Tx Freq[MHz]': '462.5625', 'Band Width': '12.5KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 2, 'Alias': 'GMRS-02', 'Rx Freq[MHz]': '462.5875', 'Tx Freq[MHz]': '462.5875', 'Band Width': '12.5KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 3, 'Alias': 'GMRS-03', 'Rx Freq[MHz]': '462.6125', 'Tx Freq[MHz]': '462.6125', 'Band Width': '12.5KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 4, 'Alias': 'GMRS-04', 'Rx Freq[MHz]': '462.6375', 'Tx Freq[MHz]': '462.6375', 'Band Width': '12.5KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 5, 'Alias': 'GMRS-05', 'Rx Freq[MHz]': '462.6625', 'Tx Freq[MHz]': '462.6625', 'Band Width': '12.5KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 6, 'Alias': 'GMRS-06', 'Rx Freq[MHz]': '462.6875', 'Tx Freq[MHz]': '462.6875', 'Band Width': '12.5KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 7, 'Alias': 'GMRS-07', 'Rx Freq[MHz]': '462.7125', 'Tx Freq[MHz]': '462.7125', 'Band Width': '12.5KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 8, 'Alias': 'GMRS-08', 'Rx Freq[MHz]': '467.5625', 'Tx Freq[MHz]': '467.5625', 'Band Width': '12.5KHz', 'TX Power': 'Low', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 9, 'Alias': 'GMRS-09', 'Rx Freq[MHz]': '467.5875', 'Tx Freq[MHz]': '467.5875', 'Band Width': '12.5KHz', 'TX Power': 'Low', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 10, 'Alias': 'GMRS-10', 'Rx Freq[MHz]': '467.6125', 'Tx Freq[MHz]': '467.6125', 'Band Width': '12.5KHz', 'TX Power': 'Low', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 11, 'Alias': 'GMRS-11', 'Rx Freq[MHz]': '467.6375', 'Tx Freq[MHz]': '467.6375', 'Band Width': '12.5KHz', 'TX Power': 'Low', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 12, 'Alias': 'GMRS-12', 'Rx Freq[MHz]': '467.6625', 'Tx Freq[MHz]': '467.6625', 'Band Width': '12.5KHz', 'TX Power': 'Low', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 13, 'Alias': 'GMRS-13', 'Rx Freq[MHz]': '467.6875', 'Tx Freq[MHz]': '467.6875', 'Band Width': '12.5KHz', 'TX Power': 'Low', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 14, 'Alias': 'GMRS-14', 'Rx Freq[MHz]': '467.7125', 'Tx Freq[MHz]': '467.7125', 'Band Width': '12.5KHz', 'TX Power': 'Low', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 15, 'Alias': 'GMRS-15', 'Rx Freq[MHz]': '462.5500', 'Tx Freq[MHz]': '462.5500', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 16, 'Alias': 'GMRS-16', 'Rx Freq[MHz]': '462.5750', 'Tx Freq[MHz]': '462.5750', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 17, 'Alias': 'GMRS-17', 'Rx Freq[MHz]': '462.6000', 'Tx Freq[MHz]': '462.6000', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 18, 'Alias': 'GMRS-18', 'Rx Freq[MHz]': '462.6250', 'Tx Freq[MHz]': '462.6250', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 19, 'Alias': 'GMRS-19', 'Rx Freq[MHz]': '462.6500', 'Tx Freq[MHz]': '462.6500', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 20, 'Alias': 'GMRS-20', 'Rx Freq[MHz]': '462.6750', 'Tx Freq[MHz]': '462.6750', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 21, 'Alias': 'GMRS-21', 'Rx Freq[MHz]': '462.7000', 'Tx Freq[MHz]': '462.7000', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 22, 'Alias': 'GMRS-22', 'Rx Freq[MHz]': '462.7250', 'Tx Freq[MHz]': '462.7250', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 23, 'Alias': 'RPT-15', 'Rx Freq[MHz]': '462.5500', 'Tx Freq[MHz]': '467.5500', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 24, 'Alias': 'RPT-16', 'Rx Freq[MHz]': '462.5750', 'Tx Freq[MHz]': '467.5750', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 25, 'Alias': 'RPT-17', 'Rx Freq[MHz]': '462.6000', 'Tx Freq[MHz]': '467.6000', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 26, 'Alias': 'RPT-18', 'Rx Freq[MHz]': '462.6250', 'Tx Freq[MHz]': '467.6250', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 27, 'Alias': 'RPT-19', 'Rx Freq[MHz]': '462.6500', 'Tx Freq[MHz]': '467.6500', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 28, 'Alias': 'RPT-20', 'Rx Freq[MHz]': '462.6750', 'Tx Freq[MHz]': '467.6750', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 29, 'Alias': 'RPT-21', 'Rx Freq[MHz]': '462.7000', 'Tx Freq[MHz]': '467.7000', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
        {'No.': 30, 'Alias': 'RPT-22', 'Rx Freq[MHz]': '462.7250', 'Tx Freq[MHz]': '467.7250', 'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF', 'TX CTCSS/DCS': 'OFF', 'Squelch Level': '4', 'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF', 'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF', 'Alarm System': 'Emergency-1', 'DTMF System': 'OFF'},
    ]

def get_output_directory():
    """Finds the next available version number and returns the directory name."""
    version = 1
    while True:
        dir_name = f"Presets-{version:02d}"
        if not os.path.isdir(dir_name):
            return dir_name
        version += 1

def choose_files_or_folders():
    """Let the user pick multiple files or a folder. Also handles drag & drop."""
    paths = []
    if len(sys.argv) > 1:
        print("Processing files from command line/drag-drop...")
        for arg in sys.argv[1:]:
            if os.path.isdir(arg):
                for f in os.listdir(arg):
                    if f.lower().endswith(".csv"):
                        paths.append(os.path.join(arg, f))
            elif arg.lower().endswith(".csv"):
                paths.append(arg)
    else:
        print("Opening file dialog...")
        root = tk.Tk()
        root.withdraw()
        paths = filedialog.askopenfilenames(
            title="Select RepeaterBook CSV File(s)",
            filetypes=[("CSV files", "*.csv")]
        )
    return list(paths)

def create_alias(call, location):
    """Creates a radio-friendly alias from a callsign and location."""
    if not call:
        call = "N/A"
    if not location:
        location = "N/A"
    alias = f"{call}-{location.strip()}"[:12]
    return alias.rstrip(" -")

def format_tone(tone_str):
    """Formats the CTCSS/DCS tone value to one decimal place."""
    if tone_str and tone_str.replace(".", "", 1).isdigit():
        tone_float = float(tone_str)
        return f"{tone_float:.1f}"
    return "OFF"

def process_files(file_state_map):
    """Reads all input files, merges them, and outputs channel/zone/scan lists."""
    output_dir = get_output_directory()
    os.makedirs(output_dir, exist_ok=True)
    print(f"--- Outputting files to new folder: {output_dir} ---")

    channel_list_filename = os.path.join(output_dir, "channel_list.csv")
    zone_filename = os.path.join(output_dir, "zone_list.csv")
    scan_filename = os.path.join(output_dir, "scan_list.csv")

    output_headers = [
        'No.', 'Alias', 'Rx Freq[MHz]', 'Tx Freq[MHz]', 'Band Width', 'TX Power', 
        'RX CTCSS/DCS', 'TX CTCSS/DCS', 'Squelch Level', 'TOT[s]', 'Tx Permission', 
        'Talkaround & Reversal', 'Compander', 'Scramble', 'Vox', 'Auto Scan System', 
        'Alarm System', 'DTMF System'
    ]

    gmrs_rows, ham_rows = [], []

    # Load GMRS from hardcoded function
    gmrs_rows = get_hardcoded_gmrs_channels()
    for row in gmrs_rows:
        row["State"] = "GMRS"
    print(f"Successfully added {len(gmrs_rows)} GMRS/VFO channels from hardcoded list.")

    for fpath, state in file_state_map.items():
        try:
            with open(fpath, mode="r", encoding="utf-8") as infile:
                reader = csv.DictReader(infile)
                processed_count = 0
                filtered_out_count = 0
                for row in reader:
                    # --- Start Filtering ---
                    mode = row.get("Mode", "").lower()
                    use = row.get("Use", "").upper()

                    # Filter 1: Mode and Use
                    if "analog" not in mode or use != "OPEN":
                        filtered_out_count += 1
                        continue
                    
                    # Filter 2: Frequency Range
                    if ENABLE_FREQUENCY_FILTER:
                        try:
                            rx_freq = float(row.get("Output Freq"))
                            tx_freq = float(row.get("Input Freq"))
                            
                            is_vhf = (VHF_RANGE[0] <= rx_freq <= VHF_RANGE[1]) and \
                                     (VHF_RANGE[0] <= tx_freq <= VHF_RANGE[1])
                            is_uhf = (UHF_RANGE[0] <= rx_freq <= UHF_RANGE[1]) and \
                                     (UHF_RANGE[0] <= tx_freq <= UHF_RANGE[1])

                            if not (is_vhf or is_uhf):
                                filtered_out_count += 1
                                continue
                        except (ValueError, TypeError):
                            # Skip row if frequencies are not valid numbers
                            filtered_out_count += 1
                            continue
                    # --- End Filtering ---

                    if not row.get("Output Freq") or not row.get("Input Freq"):
                        continue
                        
                    ham_rows.append({
                        'No.': 'HAM_PLACEHOLDER', 'Alias': create_alias(row.get('Call'), row.get('Location')),
                        'Rx Freq[MHz]': row.get('Output Freq'), 'Tx Freq[MHz]': row.get('Input Freq'),
                        'Band Width': '25KHz', 'TX Power': 'High', 'RX CTCSS/DCS': 'OFF',
                        'TX CTCSS/DCS': format_tone(row.get('Uplink Tone')), 'Squelch Level': '4',
                        'TOT[s]': '180', 'Tx Permission': 'Always', 'Talkaround & Reversal': 'OFF',
                        'Compander': 'OFF', 'Scramble': 'OFF', 'Vox': 'OFF', 'Auto Scan System': 'OFF',
                        'Alarm System': 'Emergency-1', 'DTMF System': 'OFF', 
                        'County': row.get('County'), 'State': state
                    })
                    processed_count += 1
                print(f"✅ Processed {processed_count} HAM channels from {os.path.basename(fpath)} for state {state}.")
                if filtered_out_count > 0:
                    print(f"   (Filtered out {filtered_out_count} channels based on Mode, Use, or Frequency Range)")
        except Exception as e:
            print(f"❌ Error reading {fpath}: {e}")

    # Sort HAM channels: State -> County -> Alias
    ham_rows.sort(key=lambda x: (x.get('State', ''), x.get('County', ''), x.get('Alias', '')))
    
    all_rows = gmrs_rows + ham_rows
    channel_number = 1
    # Renumber everything except VFO channels
    for row in all_rows:
        if str(row.get("No.")).upper() not in ["VFOA", "VFOB"]:
            row["No."] = channel_number
            channel_number += 1

    with open(channel_list_filename, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=output_headers)
        writer.writeheader()
        writer.writerows([{k: v for k, v in row.items() if k not in ['County', 'State']} for row in all_rows])
    print(f"\n✅ Success! Saved channel_list.csv with {len(all_rows)} total channels.")

    # --- Zone and Scan List Generation ---
    create_zone_and_scan_files(all_rows, zone_filename, scan_filename)

def create_zone_and_scan_files(all_channels, zone_filename, scan_filename):
    """Creates the zone and scan list files."""
    num_to_alias_map = {str(ch.get('No.')): ch.get('Alias') for ch in all_channels if ch.get('No.')}
    
    # Initialize zone_channels dictionary
    zone_channels = {"GMRS": []}
    used_states = {ch['State'] for ch in all_channels if ch.get('State') and ch.get('State') != 'GMRS'}
    for state in used_states:
        if state in ZONE_DEFINITIONS:
            for zone_name in ZONE_DEFINITIONS[state]:
                zone_channels[f"{state}-{zone_name}"] = []
    
    # Assign channels to zones
    for channel in all_channels:
        state, county, alias = channel.get('State'), channel.get('County'), channel.get('Alias')
        if not all([state, alias]) or alias in ['VFO-A', 'VFO-B']: continue
        
        channel_tuple = (str(channel['No.']), alias)
        if state == 'GMRS':
            zone_channels['GMRS'].append(channel_tuple)
            continue
            
        if state in ZONE_DEFINITIONS:
            found_zone = False
            for z_name, counties_str in ZONE_DEFINITIONS[state].items():
                if county in [c.strip() for c in counties_str.split(',')]:
                    zone_channels[f"{state}-{z_name}"].append(channel_tuple)
                    found_zone = True
                    break

    # --- Split oversized zones ---
    final_zones = {}
    for zone_name, channel_tuples in zone_channels.items():
        if not channel_tuples: continue
        id_list = [t[0] for t in channel_tuples]
        if len(id_list) <= ZONE_CHANNEL_LIMIT:
            final_zones[zone_name] = channel_tuples
        else:
            print(f"Zone '{zone_name}' ({len(id_list)} channels) is too large, splitting...")
            alias_groups = {}
            for ch_id, ch_alias in channel_tuples:
                alias_groups.setdefault(ch_alias, []).append(ch_id)

            sub_zones, current_sub_zone = [], []
            for alias, ids in sorted(alias_groups.items()):
                if len(current_sub_zone) + len(ids) > ZONE_CHANNEL_LIMIT and current_sub_zone:
                    sub_zones.append(current_sub_zone)
                    current_sub_zone = []
                current_sub_zone.extend([(id, alias) for id in ids])
            if current_sub_zone: sub_zones.append(current_sub_zone)
            
            for i, sub_zone_tuples in enumerate(sub_zones):
                final_zones[f"{zone_name}{chr(97 + i)}"] = sub_zone_tuples

    # --- Write zone_list.csv ---
    with open(zone_filename, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["No.", "Area Name", "AreaChannelList"])
        
        zone_no = 1
        
        # Handle GMRS first
        if 'GMRS' in final_zones:
            tuples = final_zones['GMRS']
            writer.writerow([zone_no, 'GMRS'[:12], ",".join([alias for num, alias in tuples])])
            zone_no += 1
        
        # Handle all other zones, sorted alphabetically
        other_zone_names = sorted([name for name in final_zones if name != 'GMRS'])
        
        for zone_name in other_zone_names:
            tuples = final_zones[zone_name]
            writer.writerow([zone_no, zone_name[:12], ",".join([alias for num, alias in tuples])])
            zone_no += 1
            
    print(f"✅ Success! Saved zone_list.csv")

    # --- Write scan_list.csv ---
    scan_headers = [
        'No.', 'Scan Name', 'Designated Transmission Channel', 'Scan Condition', 
        'Scan Hang Time[s]', 'Talk Back Enable', 'Scan Mode', 'Transmit Channel', 
        'Priority Channel1', 'Priority Channel2', 'Scan Channel List'
    ]
    with open(scan_filename, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=scan_headers)
        writer.writeheader()
        scan_no = 1
        
        # GMRS Scan list first
        if 'GMRS' in final_zones:
            gmrs_aliases = [alias for num, alias in final_zones['GMRS'] if alias.startswith('GMRS')]
            if gmrs_aliases:
                writer.writerow({
                    'No.': scan_no, 'Scan Name': 'ALL_GMRS',
                    'Designated Transmission Channel': 'Last Active Channel',
                    'Scan Condition': 'Carrier', 'Scan Hang Time[s]': '1', 'Talk Back Enable': 'OFF',
                    'Scan Mode': 'Carrier', 'Transmit Channel': gmrs_aliases[0],
                    'Priority Channel1': 'None', 'Priority Channel2': 'None',
                    'Scan Channel List': ",".join(gmrs_aliases)
                })
                scan_no += 1
        
        # Then other zones
        for zone_name, tuples in sorted(final_zones.items()):
            if zone_name == 'GMRS': continue
            aliases = [alias for num, alias in tuples]
            if not aliases: continue
            writer.writerow({
                'No.': scan_no, 'Scan Name': zone_name[:12],
                'Designated Transmission Channel': 'Last Active Channel',
                'Scan Condition': 'Carrier', 'Scan Hang Time[s]': '1', 'Talk Back Enable': 'OFF',
                'Scan Mode': 'Carrier', 'Transmit Channel': aliases[0],
                'Priority Channel1': 'None', 'Priority Channel2': 'None',
                'Scan Channel List': ",".join(aliases)
            })
            scan_no += 1
    print(f"✅ Success! Saved scan_list.csv")

# --- Main Execution ---
if __name__ == "__main__":
    files = choose_files_or_folders()
    if not files:
        print("❌ No files selected. Exiting.")
        sys.exit(1)

    file_state_map = {}
    for f in files:
        while True:
            state = input(f"📂 For file '{os.path.basename(f)}', enter the 2-letter state code: ").strip().upper()
            if state in ZONE_DEFINITIONS:
                file_state_map[f] = state
                break
            else:
                print(f"⚠️ State '{state}' not found in definitions. Please try again.")
    
    # Pass the full zone definitions to the processing function
    process_files(file_state_map)
    input("\nProcessing complete. Press Enter to exit.")


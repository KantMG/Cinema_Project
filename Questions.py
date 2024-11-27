0      tt0000001      0.0     1894.0  ...            NaN           5.7   2081.0
1      tt0000002      0.0     1892.0  ...            NaN           5.6    280.0
2      tt0000003      0.0     1892.0  ...            NaN           6.5   2078.0
3      tt0000004      0.0     1892.0  ...            NaN           5.4    181.0
4      tt0000005      0.0     1893.0  ...            NaN           6.2   2816.0
...          ...      ...        ...  ...            ...           ...      ...
27111  tt0414715      NaN        NaN  ...            6.0           NaN      NaN
27112  tt0414716      NaN        NaN  ...            NaN           NaN      NaN
27113  tt0414724      NaN        NaN  ...            NaN           NaN      NaN
27114  tt0414752      NaN        NaN  ...            1.0           NaN      NaN
27115  tt0414765      NaN        NaN  ...            NaN           NaN      NaN

[27116 rows x 11 columns]


inner if series is in the list

11049789
10392848
8472376
1472885
731560


           tconst  titleType  isAdult  ...  episodeNumber  averageRating numVotes
0       tt0031458  tvEpisode      0.0  ...             \N            6.9       15
1       tt0041951  tvEpisode      0.0  ...              9            7.6       94
2       tt0042816  tvEpisode      0.0  ...             17            7.6       12
3       tt0044093  tvEpisode      0.0  ...              6            4.4       20
4       tt0045960  tvEpisode      0.0  ...              3            6.9      197
...           ...        ...      ...  ...            ...            ...      ...
731555  tt9916708  tvEpisode      0.0  ...             48            8.4        8
731556  tt9916766  tvEpisode      0.0  ...             15            7.1       24
731557  tt9916778  tvEpisode      0.0  ...              3            7.2       37
731558  tt9916840  tvEpisode      0.0  ...              1            7.2       10
731559  tt9916880  tvEpisode      0.0  ...              2            8.6        8

[731560 rows x 12 columns]


inner if series is not in the list


11049789
10392848
1472885
1459335


            tconst  titleType  ...  averageRating  numVotes
0        tt0000001      short  ...            5.7      2081
1        tt0000002      short  ...            5.6       280
2        tt0000003      short  ...            6.5      2078
3        tt0000004      short  ...            5.4       181
4        tt0000005      short  ...            6.2      2816
...            ...        ...  ...            ...       ...
1459330  tt9916730      movie  ...            7.0        12
1459331  tt9916766  tvEpisode  ...            7.1        24
1459332  tt9916778  tvEpisode  ...            7.2        37
1459333  tt9916840  tvEpisode  ...            7.2        10
1459334  tt9916880  tvEpisode  ...            8.6         8

[1459335 rows x 9 columns]



outer if series is not in the list


11049789
10392848
1472885
11240219


             tconst  titleType  ...  averageRating  numVotes
0         tt0000001      short  ...            5.7    2081.0
1         tt0000002      short  ...            5.6     280.0
2         tt0000003      short  ...            6.5    2078.0
3         tt0000004      short  ...            5.4     181.0
4         tt0000005      short  ...            6.2    2816.0
...             ...        ...  ...            ...       ...
11240214  tt9916848  tvEpisode  ...            NaN       NaN
11240215  tt9916850  tvEpisode  ...            NaN       NaN
11240216  tt9916852  tvEpisode  ...            NaN       NaN
11240217  tt9916856      short  ...            NaN       NaN
11240218  tt9916880  tvEpisode  ...            8.6       8.0

[11240219 rows x 9 columns]


outer if series is in the list


11049789
10392848
8472376
1472885
11240219

             tconst  titleType  isAdult  ...  episodeNumber  averageRating numVotes
0         tt0000001      short      0.0  ...            NaN            5.7   2081.0
1         tt0000002      short      0.0  ...            NaN            5.6    280.0
2         tt0000003      short      0.0  ...            NaN            6.5   2078.0
3         tt0000004      short      0.0  ...            NaN            5.4    181.0
4         tt0000005      short      0.0  ...            NaN            6.2   2816.0
...             ...        ...      ...  ...            ...            ...      ...
11240214  tt9916848  tvEpisode      0.0  ...             17            NaN      NaN
11240215  tt9916850  tvEpisode      0.0  ...             19            NaN      NaN
11240216  tt9916852  tvEpisode      0.0  ...             20            NaN      NaN
11240217  tt9916856      short      0.0  ...            NaN            NaN      NaN
11240218  tt9916880  tvEpisode      0.0  ...              2            8.6      8.0

[11240219 rows x 12 columns]
import re
import pandas as pd

# pega aquí TODO tu texto entre triple comillas
raw_text = """
1
undefined Logo
Cameron Ward
QB
Miami (FL)
1
Titans Logo
TEN
2
undefined Logo
Travis Hunter
CB
Colorado
2
Browns Logo
CLE
3
undefined Logo
Abdul Carter
EDGE
Penn State
3
Giants Logo
NYG
4
undefined Logo
Will Campbell
OT
LSU
4
Patriots Logo
NE
5
undefined Logo
Ashton Jeanty
RB
Boise State
5
Jaguars Logo
JAC
6
undefined Logo
Mason Graham
DL
Michigan
7
undefined Logo
Armand Membou
OT
Missouri
6
Raiders Logo
LV
8
undefined Logo
Tyler Warren
TE
Penn State
7
Jets Logo
NYJ
9
undefined Logo
Jalon Walker
EDGE
Georgia
8
Panthers Logo
CAR
10
undefined Logo
Tetairoa McMillan
WR
Arizona
12
Cowboys Logo
DAL
11
undefined Logo
Kelvin Banks
OT
Texas
10
Bears Logo
CHI
12
undefined Logo
Shedeur Sanders
QB
Colorado
9
Saints Logo
NO
13
undefined Logo
Will Johnson
CB
Michigan
16
Cardinals Logo
ARI
14
undefined Logo
Mykel Williams
EDGE
Georgia
15
undefined Logo
Colston Loveland
TE
Michigan
14
Colts Logo
IND
16
undefined Logo
Jahdae Barron
CB
Texas
13
Dolphins Logo
MIA
17
undefined Logo
Mike Green
EDGE
Marshall
15
Falcons Logo
ATL
18
undefined Logo
Matthew Golden
WR
Texas
19
undefined Logo
Shemar Stewart
EDGE
Texas A&M
20
undefined Logo
Walter Nolen
DL
Mississippi
11
49ers Logo
SF
21
undefined Logo
Jihaad Campbell
LB
Alabama
19
Buccaneers Logo
TB
22
undefined Logo
Omarion Hampton
RB
North Carolina
20
Broncos Logo
DEN
23
undefined Logo
Malaki Starks
S
Georgia
27
Ravens Logo
BAL
24
undefined Logo
Kenneth Grant
DL
Michigan
22
Chargers Logo
LAC
1
25
undefined Logo
Grey Zabel
IOL
North Dakota State
18
Seahawks Logo
SEA
1
26
undefined Logo
Josh Simmons
OT
Ohio State
25
Texans Logo
HOU
27
undefined Logo
Derrick Harmon
DL
Oregon
17
Bengals Logo
CIN
28
undefined Logo
Tyler Booker
IOL
Alabama
29
undefined Logo
Donovan Ezeiruaku
EDGE
Boston College
28
Lions Logo
DET
30
undefined Logo
Nick Emmanwori
S
South Carolina
24
Vikings Logo
MIN
31
undefined Logo
Emeka Egbuka
WR
Ohio State
32
undefined Logo
James Pearce Jr.
EDGE
Tennessee
29
Commanders Logo
WAS
33
undefined Logo
Jaxson Dart
QB
Mississippi
21
Steelers Logo
PIT
34
undefined Logo
Maxwell Hairston
CB
Kentucky
23
Packers Logo
GB
35
undefined Logo
Josh Conerly Jr.
OT
Oregon
31
Chiefs Logo
KC
36
undefined Logo
Luther Burden
WR
Missouri
37
undefined Logo
TreVeyon Henderson
RB
Ohio State
38
undefined Logo
Trey Amos
CB
Mississippi
26
Rams Logo
LAR
39
undefined Logo
Donovan Jackson
IOL
Ohio State
40
undefined Logo
Jalen Milroe
QB
Alabama
41
undefined Logo
Nic Scourton
EDGE
Texas A&M
32
Eagles Logo
PHI
42
undefined Logo
Shavon Revel Jr.
CB
East Carolina
30
Bills Logo
BUF
43
undefined Logo
Mason Taylor
TE
LSU
44
undefined Logo
Tyleik Williams
DL
Ohio State
45
undefined Logo
Aireontae Ersery
OT
Minnesota
46
undefined Logo
Carson Schwesinger
LB
UCLA
1
47
undefined Logo
Jayden Higgins
WR
Iowa State
1
48
undefined Logo
Benjamin Morrison
CB
Notre Dame
49
undefined Logo
Xavier Watts
S
Notre Dame
50
undefined Logo
J.T. Tuimoloau
EDGE
Ohio State
51
undefined Logo
Darius Alexander
DL
Toledo
52
undefined Logo
Azareye'h Thomas
CB
Florida State
53
undefined Logo
Landon Jackson
EDGE
Arkansas
54
undefined Logo
Quinshon Judkins
RB
Ohio State
55
undefined Logo
Jonah Savaiinaea
IOL
Arizona
56
undefined Logo
Kaleb Johnson
RB
Iowa
57
undefined Logo
Oluwafemi Oladejo
EDGE
UCLA
4
58
undefined Logo
Elijah Arroyo
TE
Miami (FL)
59
undefined Logo
T.J. Sanders
DL
South Carolina
60
undefined Logo
Jaylin Noel
WR
Iowa State
61
undefined Logo
Tate Ratledge
IOL
Georgia
4
62
undefined Logo
Princely Umanmielen
EDGE
Mississippi
63
undefined Logo
Tre Harris
WR
Mississippi
64
undefined Logo
Alfred Collins
DL
Texas
1
65
undefined Logo
Marcus Mbow
IOL
Purdue
1
66
undefined Logo
Jordan Burch
EDGE
Oregon
2
67
undefined Logo
Jack Sawyer
EDGE
Ohio State
68
undefined Logo
Darien Porter
CB
Iowa State
69
undefined Logo
Kevin Winston Jr.
S
Penn State
70
undefined Logo
Tyler Shough
QB
Louisville
71
undefined Logo
Bradyn Swinson
EDGE
LSU
72
undefined Logo
Jack Bech
WR
TCU
73
undefined Logo
Elic Ayomanor
WR
Stanford
74
undefined Logo
Kyle Williams
WR
Washington State
1
75
undefined Logo
Josaiah Stewart
EDGE
Michigan
1
76
undefined Logo
Jalen Royals
WR
Utah State
77
undefined Logo
Harold Fannin Jr.
TE
Bowling Green
78
undefined Logo
Omarr Norman-Lott
DL
Tennessee
1
79
undefined Logo
Andrew Mukuba
S
Texas
2
80
undefined Logo
Jared Wilson
IOL
Georgia
81
undefined Logo
Wyatt Milum
OT
West Virginia
3
82
undefined Logo
Shemar Turner
DL
Texas A&M
83
undefined Logo
Demetrius Knight
LB
South Carolina
84
undefined Logo
Terrance Ferguson
TE
Oregon
85
undefined Logo
Ozzy Trapilo
OT
Boston College
86
undefined Logo
Joshua Farmer
DL
Florida State
87
undefined Logo
Charles Grant
IOL
William & Mary
88
undefined Logo
Jacob Parrish
CB
Kansas State
89
undefined Logo
Kyle Kennard
EDGE
South Carolina
90
undefined Logo
Dylan Sampson
RB
Tennessee
91
undefined Logo
Cameron Skattebo
RB
Arizona State
92
undefined Logo
Ashton Gillotte
EDGE
Louisville
93
undefined Logo
Ty Robinson
DL
Nebraska
94
undefined Logo
Emery Jones Jr.
OT
LSU
95
undefined Logo
Deone Walker
DL
Kentucky
96
undefined Logo
Savion Williams
WR
TCU
97
undefined Logo
Anthony Belton
OT
NC State
98
undefined Logo
Nohl Williams
CB
California
1
99
undefined Logo
Cameron Williams
OT
Texas
1
100
undefined Logo
Quincy Riley
CB
Louisville
101
undefined Logo
Damien Martinez
RB
Miami (FL)
1
102
undefined Logo
Will Howard
QB
Ohio State
1
103
undefined Logo
Tory Horton
WR
Colorado State
104
undefined Logo
Danny Stutsman
LB
Oklahoma
105
undefined Logo
C.J. West
DL
Indiana
106
undefined Logo
Billy Bowman
S
Oklahoma
107
undefined Logo
D.J. Giddens
RB
Kansas State
1
108
undefined Logo
Lathan Ransom
S
Ohio State
1
109
undefined Logo
Gunnar Helm
TE
Texas
110
undefined Logo
R.J. Harvey Jr.
RB
UCF
111
undefined Logo
Jamaree Caldwell
DL
Oregon
112
undefined Logo
Jason Marshall Jr.
CB
Florida
113
undefined Logo
Tai Felton
WR
Maryland
114
undefined Logo
Chris Paul Jr.
LB
Mississippi
115
undefined Logo
Jonas Sanker
S
Virginia
116
undefined Logo
Miles Frazier
IOL
LSU
117
undefined Logo
Smael Mondon Jr.
LB
Georgia
1
118
undefined Logo
Dylan Fairchild
IOL
Georgia
2
119
undefined Logo
Jaylen Reed
S
Penn State
120
undefined Logo
Bhayshul Tuten
RB
Virginia Tech
3
121
undefined Logo
Denzel Burke
CB
Ohio State
122
undefined Logo
Dorian Strong
CB
Virginia Tech
123
undefined Logo
Quinn Ewers
QB
Texas
124
undefined Logo
Jordan James
RB
Oregon
1
125
undefined Logo
Jared Ivey
EDGE
Mississippi
1
126
undefined Logo
Devin Neal
RB
Kansas
127
undefined Logo
Jordan Phillips
DL
Maryland
128
undefined Logo
Tez Johnson
WR
Oregon
129
undefined Logo
Barrett Carter
LB
Clemson
1
130
undefined Logo
Zah Frazier
CB
UTSA
1
131
undefined Logo
Isaiah Bond
WR
Texas
132
undefined Logo
Kyle McCord
QB
Syracuse
133
undefined Logo
Chase Lundt
OT
UConn
1
134
undefined Logo
Aeneas Peebles
DL
Virginia Tech
1
135
undefined Logo
David Walker
EDGE
Central Arkansas
1
136
undefined Logo
Jeffrey Bassa
LB
Oregon
1
137
undefined Logo
Xavier Restrepo
WR
Miami (FL)
138
undefined Logo
Cody Simon
LB
Ohio State
139
undefined Logo
Jaydon Blue
RB
Texas
2
140
undefined Logo
Trevor Etienne
RB
Georgia
1
141
undefined Logo
Malachi Moore
S
Alabama
1
142
undefined Logo
Saivion Jones
EDGE
LSU
143
undefined Logo
Barryn Sorrell
EDGE
Texas
144
undefined Logo
Ty Hamilton
DL
Ohio State
145
undefined Logo
Brashard Smith
RB
SMU
146
undefined Logo
Jalen Rivers
OT
Miami (FL)
147
undefined Logo
Seth McLaughlin
IOL
Ohio State
2
148
undefined Logo
Jalen Travis
OT
Iowa State
1
149
undefined Logo
Cobee Bryant
CB
Kansas
1
150
undefined Logo
Caleb Ransaw
S
Tulane
151
undefined Logo
Mitchell Evans
TE
Notre Dame
2
152
undefined Logo
Rylie Mills
DL
Notre Dame
1
153
undefined Logo
Vernon Broughton
DL
Texas
1
154
undefined Logo
Elijah Roberts
DL
SMU
1
155
undefined Logo
Antwaun Powell-Ryland
EDGE
Virginia Tech
1
156
undefined Logo
J.J. Pegues
DL
Mississippi
157
undefined Logo
Zy Alexander
CB
LSU
158
undefined Logo
Ollie Gordon II
RB
Oklahoma State
1
159
undefined Logo
Jack Kiser
LB
Notre Dame
1
160
undefined Logo
Logan Brown
OT
Kansas
161
undefined Logo
Jackson Slater
IOL
Sacramento State
1
162
undefined Logo
Pat Bryant
WR
Illinois
1
163
undefined Logo
R.J. Mickens
S
Clemson
1
164
undefined Logo
Ajani Cornelius
OT
Oregon
2
165
undefined Logo
Jordan Hancock
CB
Ohio State
4
166
undefined Logo
Oronde Gadsden II
TE
Syracuse
3
167
undefined Logo
Teddye Buchanan
LB
California
1
168
undefined Logo
Isaac TeSlaa
WR
Arkansas
1
169
undefined Logo
Jaylin Lane
WR
Virginia Tech
1
170
undefined Logo
Nick Martin
LB
Oklahoma State
3
171
undefined Logo
Dont'e Thornton
WR
Tennessee
3
172
undefined Logo
Tyrion Ingram-Dawkins
EDGE
Georgia
173
undefined Logo
Kobe King
LB
Penn State
8
174
undefined Logo
Carson Vinson
IOL
Alabama A&M
3
175
undefined Logo
Upton Stout
CB
Western Kentucky
3
176
undefined Logo
Jarquez Hunter
RB
Auburn
1
177
undefined Logo
Cam Jackson
DL
Florida
178
undefined Logo
Dillon Gabriel
QB
Oregon
2
179
undefined Logo
Tyler Baron
EDGE
Miami (FL)
3
180
undefined Logo
Hollin Pierce
OT
Rutgers
1
181
undefined Logo
Luke Kandra
IOL
Cincinnati
2
182
undefined Logo
Caleb Rogers
IOL
Texas Tech
1
183
undefined Logo
Sebastian Castro
S
Iowa
1
184
undefined Logo
Drew Kendall
IOL
Boston College
185
undefined Logo
Fadil Diggs
EDGE
Syracuse
1
186
undefined Logo
Justin Walley
CB
Minnesota
2
187
undefined Logo
Joshua Gray
IOL
Oregon State
3
188
undefined Logo
Craig Woodson
S
California
1
189
undefined Logo
Que Robinson
EDGE
Alabama
2
190
undefined Logo
Jah Joyner
EDGE
Minnesota
5
191
undefined Logo
LeQuint Allen Jr.
RB
Syracuse
2
192
undefined Logo
Jake Majors
IOL
Texas
1
193
undefined Logo
Jackson Hawes
TE
Georgia Tech
1
194
undefined Logo
Thomas Fidone II
TE
Nebraska
195
undefined Logo
Bilhal Kone
CB
Western Michigan
1
196
undefined Logo
Jack Nelson
OT
Wisconsin
1
197
undefined Logo
Riley Leonard
QB
Notre Dame
1
198
undefined Logo
Hunter Wohler
S
Wisconsin
1
199
undefined Logo
Jalin Conyers
TE
Texas Tech
200
undefined Logo
Jake Briningstool
TE
Clemson
1
201
undefined Logo
Tommi Hill
CB
Nebraska
1
202
undefined Logo
Jo'Quavious Marks
RB
USC
2
203
undefined Logo
Kain Medrano
LB
UCLA
2
204
undefined Logo
Nick Nash
WR
San Jose State
2
205
undefined Logo
Mac McWilliams
S
UCF
2
206
undefined Logo
Shemar James
LB
Florida
2
207
undefined Logo
Willie Lampkin
IOL
North Carolina
2
208
undefined Logo
Collin Oliver
EDGE
Oklahoma State
1
209
undefined Logo
Yahya Black
DL
Iowa
1
210
undefined Logo
Kyle Monangai
RB
Rutgers
2
211
undefined Logo
Maxen Hook
S
Toledo
1
212
undefined Logo
Jabbar Muhammad
CB
Oregon
1
213
undefined Logo
Myles Hinton
OT
Michigan
214
undefined Logo
Luke Lachey
TE
Iowa
2
215
undefined Logo
Korie Black
CB
Oklahoma State
1
216
undefined Logo
Tahj Brooks
RB
Texas Tech
1
217
undefined Logo
Raheim Sanders
RB
South Carolina
1
218
undefined Logo
Keandre Lambert-Smith
WR
Auburn
3
219
undefined Logo
Bryce Cabeldue
IOL
Kansas
220
undefined Logo
Jaylin Smith
CB
USC
1
221
undefined Logo
Kitan Crawford
S
Nevada
1
222
undefined Logo
Tonka Hemingway
DL
South Carolina
223
undefined Logo
Connor Colby
IOL
Iowa
224
undefined Logo
Chimere Dike
WR
Florida
1
225
undefined Logo
Jay Higgins
LB
Iowa
1
226
undefined Logo
Andrew Armstrong
WR
Arkansas
1
227
undefined Logo
Mello Dotson
CB
Kansas
1
228
undefined Logo
Kaimon Rucker
EDGE
North Carolina
1
229
undefined Logo
Howard Cross III
DL
Notre Dame
1
230
undefined Logo
Robert Longerbeam
CB
Rutgers
1
231
undefined Logo
Kalel Mullings
RB
Michigan
3
232
undefined Logo
Jay Toia
DL
UCLA
233
undefined Logo
Donovan Edwards
RB
Michigan
1
234
undefined Logo
Elijhah Badger
WR
Florida
1
235
undefined Logo
Kobe Hudson
WR
UCF
236
undefined Logo
Alijah Huzzie
CB
North Carolina
237
undefined Logo
Tyler Batty
EDGE
BYU
2
238
undefined Logo
Jimmy Horn Jr.
WR
Colorado
239
undefined Logo
Clay Webb
IOL
Jacksonville State
2
240
undefined Logo
Ricky White
WR
UNLV
2
241
undefined Logo
Ahmed Hassanein
DL
Boise State
242
undefined Logo
Garrett Dellinger
IOL
LSU
2
243
undefined Logo
Dante Trader Jr.
S
Maryland
3
244
undefined Logo
Cam Horsley
DL
Boston College
1
245
undefined Logo
Jermari Harris
CB
Iowa
1
246
undefined Logo
Nazir Stackhouse
DL
Georgia
3
247
undefined Logo
Cody Lindenberg
LB
Minnesota
248
undefined Logo
Brandon Crenshaw-Dickson
OT
Florida
1
249
undefined Logo
Dan Jackson
S
Georgia
2
250
undefined Logo
Moliki Matavao
TE
UCLA
2
251
undefined Logo
Tim Smith
DL
Alabama
1
252
undefined Logo
Eli Cox
IOL
Kentucky
253
undefined Logo
Benjamin Yurosek
TE
Georgia
1
254
undefined Logo
Warren Brinson
DL
Georgia
3
255
undefined Logo
Xavier Truss
OT
Georgia
2
256
undefined Logo
C.J. Dippre
TE
Alabama
257
undefined Logo
Marcus Yarns
RB
Delaware
2
258
undefined Logo
Phil Mafah
RB
Clemson
259
undefined Logo
Isaiah Neyor
WR
Nebraska
260
undefined Logo
Ryan Fitzgerald
K
Florida State
2
261
undefined Logo
Simeon Barrow Jr.
DL
Miami (FL)
2
262
undefined Logo
Jared Harrison-Hunte
DL
SMU
2
263
undefined Logo
Jamon Dumas-Johnson
LB
Kentucky
4
264
undefined Logo
Joshua Simon
TE
South Carolina
3
265
undefined Logo
Marques Sigle
S
Kansas State
1
266
undefined Logo
Carson Bruener
LB
Washington
1
267
undefined Logo
Kaden Prather
WR
Maryland
2
268
undefined Logo
Eugene Asante
LB
Auburn
2
269
undefined Logo
Max Brosmer
QB
Minnesota
2
270
undefined Logo
Rayuan Lane III
S
Navy
2
271
undefined Logo
Ja'Corey Brooks
WR
Louisville
1
272
undefined Logo
Junior Tafuna
DL
Utah
2
273
undefined Logo
Jacory Croskey-Merritt
RB
Arizona
274
undefined Logo
Arian Smith
WR
Georgia
2
275
undefined Logo
Andres Borregales
K
Miami (FL)
7
276
undefined Logo
Kurtis Rourke
QB
Indiana
3
277
undefined Logo
Shaun Dolac
LB
Buffalo
2
278
undefined Logo
Bru McCoy
WR
Tennessee
1
279
undefined Logo
John Williams
OT
Cincinnati
1
280
undefined Logo
Brandon Adams
CB
UCF
2
281
undefined Logo
Corey Kiner
RB
Cincinnati
1
282
undefined Logo
Efton Chism III
WR
Eastern Washington
1
283
undefined Logo
Joe Huber
IOL
Wisconsin
284
undefined Logo
Jordan Watkins
WR
Mississippi
285
undefined Logo
Will Sheppard
WR
Colorado
2
286
undefined Logo
Konata Mumpfield
WR
Pittsburgh
287
undefined Logo
Dean Clark
S
Fresno State
1
288
undefined Logo
Samuel Brown
WR
Miami (FL)
3
289
undefined Logo
LaJohntay Wester
WR
Colorado
1
290
undefined Logo
Jackson Woodard
LB
UNLV
1
291
undefined Logo
Brady Cook
QB
Missouri
2
292
undefined Logo
Montrell Johnson
RB
Florida
4
293
undefined Logo
Theo Wease
WR
Missouri
294
undefined Logo
Zeek Biggers
DL
Georgia Tech
3
295
undefined Logo
Elijah Ponder
EDGE
Cal Poly
1
296
undefined Logo
R.J. Oben
EDGE
Notre Dame
4
297
undefined Logo
Hayden Conner
IOL
Texas
2
298
undefined Logo
Seth Henigan
QB
Memphis
1
299
undefined Logo
Thomas Perry
IOL
Middlebury
1
300
undefined Logo
Dominic Lovett
WR


"""

lines = [l.strip() for l in raw_text.split("\n") if l.strip()]


i = 0
players = []

VALID_POS = {
    "QB","RB","WR","TE",
    "OT","OL","IOL","G","C",
    "EDGE","DL","DT",
    "CB","S","LB"
}

for i in range(len(lines)):
    # buscamos línea que sea posición
    pos = lines[i].strip().upper()

    if pos in VALID_POS:
        try:
            name = lines[i-1]
            
            # buscar hacia atrás el rank
            j = i - 2
            while j >= 0:
                if re.match(r"^\d+$", lines[j]):
                    rank = int(lines[j])
                    break
                j -= 1

            players.append({
                "name": name,
                "position": pos,
                "rank": rank
            })

        except:
            continue

df = pd.DataFrame(players)

if df.empty:
    print("❌ No se han detectado jugadores. Revisa el parsing.")
    exit()

df = df.drop_duplicates(subset=["name"])
df = df.sort_values("rank")

df.to_csv("big_board_2025.csv", index=False)

print(df.head(20))
print(f"\nTotal jugadores: {len(df)}")
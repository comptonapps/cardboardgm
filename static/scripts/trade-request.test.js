beforeAll(function() {
    cardInfo = {title: "1951 Bowman #305 Willie Mays PSA 4", id: 20, full_url: "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1951/305/20/large.JPEG"}

    testCards = [
        {
          "description": "PSA 10",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1989/33/4/large.JPEG",
          "id": 4,
          "number": "33",
          "player": "Ken Griffey Jr",
          "set_name": "Donruss",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1989/33/4/thumb.JPEG",
          "title": "1989 Donruss #33 Ken Griffey Jr PSA 10",
          "year": 1989
        },
        {
          "description": "PSA 8",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1971/630/24/large.JPEG",
          "id": 24,
          "number": "630",
          "player": "Roberto Clemente",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1971/630/24/thumb.JPEG",
          "title": "1971 Topps #630 Roberto Clemente PSA 8",
          "year": 1971
        },
        {
          "description": "PSA 5",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1970/189/23/large.JPEG",
          "id": 23,
          "number": "189",
          "player": "Thurman Munson",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1970/189/23/thumb.JPEG",
          "title": "1970 Topps #189 Thurman Munson PSA 5",
          "year": 1970
        },
        {
          "description": "PSA 7.5 NM+",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1968/177/22/large.JPEG",
          "id": 22,
          "number": "177",
          "player": "Nolan Ryan",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1968/177/22/thumb.JPEG",
          "title": "1968 Topps #177 Nolan Ryan PSA 7.5 NM+",
          "year": 1968
        },
        {
          "description": "Excellent",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1962/387/25/large.JPEG",
          "id": 25,
          "number": "387",
          "player": "Lou Brock",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1962/387/25/thumb.JPEG",
          "title": "1962 Topps #387 Lou Brock Excellent",
          "year": 1962
        },
        {
          "description": "BVG 6",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1960/148/26/large.JPEG",
          "id": 26,
          "number": "148",
          "player": "Carl Yastrzemski",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1960/148/26/thumb.JPEG",
          "title": "1960 Topps #148 Carl Yastrzemski BVG 6",
          "year": 1960
        },
        {
          "description": "PSA 8.5",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1958/1/16/large.JPEG",
          "id": 16,
          "number": "1",
          "player": "Ted Williams",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1958/1/16/thumb.JPEG",
          "title": "1958 Topps #1 Ted Williams PSA 8.5",
          "year": 1958
        },
        {
          "description": "PSA 7",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1957/1/15/large.JPEG",
          "id": 15,
          "number": "1",
          "player": "Ted Williams",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1957/1/15/thumb.JPEG",
          "title": "1957 Topps #1 Ted Williams PSA 7",
          "year": 1957
        },
        {
          "description": "PSA 6",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1956/5/14/large.JPEG",
          "id": 14,
          "number": "5",
          "player": "Ted Williams",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1956/5/14/thumb.JPEG",
          "title": "1956 Topps #5 Ted Williams PSA 6",
          "year": 1956
        },
        {
          "description": "VG-EX",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1955/194/13/large.JPEG",
          "id": 13,
          "number": "194",
          "player": "Willie Mays",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1955/194/13/thumb.JPEG",
          "title": "1955 Topps #194 Willie Mays VG-EX",
          "year": 1955
        },
        {
          "description": "PSA 6.5",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1955/123/12/large.JPEG",
          "id": 12,
          "number": "123",
          "player": "Sandy Koufax",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1955/123/12/thumb.JPEG",
          "title": "1955 Topps #123 Sandy Koufax PSA 6.5",
          "year": 1955
        },
        {
          "description": "BVG 4",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1955/164/11/large.JPEG",
          "id": 11,
          "number": "164",
          "player": "Roberto Clemente",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1955/164/11/thumb.JPEG",
          "title": "1955 Topps #164 Roberto Clemente BVG 4",
          "year": 1955
        },
        {
          "description": "PSA 7",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1954/128/10/large.JPEG",
          "id": 10,
          "number": "128",
          "player": "Hank Aaron",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1954/128/10/thumb.JPEG",
          "title": "1954 Topps #128 Hank Aaron PSA 7",
          "year": 1954
        },
        {
          "description": "Near Mint",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1954/89/9/large.JPEG",
          "id": 9,
          "number": "89",
          "player": "Willie Mays",
          "set_name": "Bowman",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1954/89/9/thumb.JPEG",
          "title": "1954 Bowman #89 Willie Mays Near Mint",
          "year": 1954
        },
        {
          "description": "Very Good",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1953/244/8/large.JPEG",
          "id": 8,
          "number": "244",
          "player": "Willie Mays",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1953/244/8/thumb.JPEG",
          "title": "1953 Topps #244 Willie Mays Very Good",
          "year": 1953
        },
        {
          "description": "PSA 5 EX",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1953/59/21/large.JPEG",
          "id": 21,
          "number": "59",
          "player": "Mickey Mantle",
          "set_name": "Bowman",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1953/59/21/thumb.JPEG",
          "title": "1953 Bowman #59 Mickey Mantle PSA 5 EX",
          "year": 1953
        },
        {
          "description": "Authentic",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1952/311/5/large.JPEG",
          "id": 5,
          "number": "311",
          "player": "Mickey Mantle",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1952/311/5/thumb.JPEG",
          "title": "1952 Topps #311 Mickey Mantle Authentic",
          "year": 1952
        },
        {
          "description": "PSA 4",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1952/261/7/large.JPEG",
          "id": 7,
          "number": "261",
          "player": "Willie Mays",
          "set_name": "Topps",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1952/261/7/thumb.JPEG",
          "title": "1952 Topps #261 Willie Mays PSA 4",
          "year": 1952
        },
        {
          "description": "PSA 4",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1951/305/20/large.JPEG",
          "id": 20,
          "number": "305",
          "player": "Willie Mays",
          "set_name": "Bowman",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1951/305/20/thumb.JPEG",
          "title": "1951 Bowman #305 Willie Mays PSA 4",
          "year": 1951
        },
        {
          "description": "PSA 6 EX-MT",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1949/224/19/large.JPEG",
          "id": 19,
          "number": "224",
          "player": "Satchel Paige",
          "set_name": "Bowman",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1949/224/19/thumb.JPEG",
          "title": "1949 Bowman #224 Satchel Paige PSA 6 EX-MT",
          "year": 1949
        },
        {
          "description": "PSA 1 Poor",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1948/6/18/large.JPEG",
          "id": 18,
          "number": "6",
          "player": "Yogi Berra",
          "set_name": "Bowman",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1948/6/18/thumb.JPEG",
          "title": "1948 Bowman #6 Yogi Berra PSA 1 Poor",
          "year": 1948
        },
        {
          "description": "PSA 4",
          "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1948/36/17/large.JPEG",
          "id": 17,
          "number": "36",
          "player": "Stan Musial",
          "set_name": "Bowman",
          "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1948/36/17/thumb.JPEG",
          "title": "1948 Bowman #36 Stan Musial PSA 4",
          "year": 1948
        }
      ]
}) 
    


describe('getFilteredResults Tests', function(){
    it ('should be equal', function() {
        expect(getFilteredResults(testCards, ['brock']).length).toEqual(1);
        expect(getFilteredResults(testCards, ['zzzzzz'])).toEqual([]);
        expect(getFilteredResults(testCards, ['ro', 'clemente'])).toEqual([{
                                                                        "description": "PSA 8",
                                                                        "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1971/630/24/large.JPEG",
                                                                        "id": 24,
                                                                        "number": "630",
                                                                        "player": "Roberto Clemente",
                                                                        "set_name": "Topps",
                                                                        "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1971/630/24/thumb.JPEG",
                                                                        "title": "1971 Topps #630 Roberto Clemente PSA 8",
                                                                        "year": 1971
                                                                      },  {
                                                                        "description": "BVG 4",
                                                                        "full_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1955/164/11/large.JPEG",
                                                                        "id": 11,
                                                                        "number": "164",
                                                                        "player": "Roberto Clemente",
                                                                        "set_name": "Topps",
                                                                        "thumb_url": "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1955/164/11/thumb.JPEG",
                                                                        "title": "1955 Topps #164 Roberto Clemente BVG 4",
                                                                        "year": 1955
                                                                      }])
    });
    it ('should return an array', function() {
        expect(getFilteredResults(testCards, ['jjjjjj'])).toBeInstanceOf(Array);
        expect(getFilteredResults(testCards, ['griff'])).toBeInstanceOf(Array);
    })

})

describe('getCardFromJson tests', function(){
    it ('should return card info', function() {
        expect(getCardFromJson(20)).toEqual({title: "1951 Bowman #305 Willie Mays PSA 4", id: 20, full_url: "https://cardboardgmpics.s3-us-west-2.amazonaws.com/cards/1951/305/20/large.JPEG"})
    })
})

describe('getNewRequestCell tests', function(){
    it ('should return a request cell', function(){
        expect(getNewRequestCell(cardInfo)).toHaveClass('request-cell')
        expect(getNewRequestCell(cardInfo)).toHaveClass('selected')
        expect(getNewRequestCell(cardInfo).innerHTML).toContain("1951 Bowman #305 Willie Mays PSA 4")
    })
    
})

describe('getCollectionItems tests', function() {
    it ('should return a p with "No Results Found', function(){
        expect(getCollectionItems([]).length).toEqual(1);
        expect(getCollectionItems([])[0].innerHTML).toContain('No Results Found');
    })

    it ('should return an array with 3 cells', function(){
        expect(getCollectionItems([testCards[0], testCards[1], testCards[2]])).toHaveSize(3);
    })
})


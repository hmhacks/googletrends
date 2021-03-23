"""
This script creates a state level Google search query dataset.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/8/2021
"""
from pytrends.request import TrendReq
import time
import pandas as pd
import GoogleTrendsCleaning as GTC
import requests

pytrends = TrendReq()

# stateList = ['NY', 'IL']

stateList = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def getGoogleTrends(termList, yearStart, yearEnd):
    """
    Returns desired dataset of Google search queries over time.

    Parameter termList represents the search terms to request.
    Preconditon: termList a list of strings

    Parameter yearStart is the lower bound of the time series.
    Preconditon: yearStart is an int

    Parameter yearEnd is the upper bound of the time series.
    Preconditon: yearEnd is an int
    """
    assert type(termList) == list

    for term in termList:
        assert type(term) == str

    #Determine sleep time between term requests
    months = 12
    googleLimit = 50000
    timeframe = months*(yearEnd - yearStart)

    accum = pd.DataFrame()
    iter = 0
    for x in range(len(termList)):
        for y in range(len(stateList)):

            stateQuery = 'US-' + stateList[y]

            if (iter + 1)* timeframe < googleLimit:

                data = makeRequest([termList[x]], yearStart, yearEnd, stateQuery)
                data['State'] = stateList[y]
                accum = accum.append(data)

                iter += 1

            # else:
            #     time.sleep(90000)
            #     data = makeRequest([termList[x]], yearStart, yearEnd, stateQuery)
            #     data['State'] = stateList[y]
            #     accum = accum.append(data)
            #     iter = 1

        filename = '../Data/SearchTerms/' + termList[x] + '.csv'
        accum.to_csv(filename, index=True, encoding='utf_8_sig')
        accum = pd.DataFrame()


def makeRequest(term, yearStart, yearEnd, stateQuery):
    """
    Builds payload and makes request to Google Trends API.
    Returns request data.

    Parameter term is the kw_list parameter being requested.
    Preconditon term is a list with len 1 (one word at at time)

    Parameter yearStart is the lower bound of the time series.
    Preconditon: yearStart is an int

    Parameter yearEnd is the upper bound of the time series.
    Preconditon: yearEnd is an int

    Parameter stateQuery is the state parameter being requested
    Preconditon: stateQuery is a string of format "US-NY", eg.
    """
    try:
        pytrends.build_payload(
             kw_list=term,
             cat=0,
             timeframe=  str(yearStart) + '-01-01 ' + str(yearEnd) + '-01-01',
             geo=stateQuery,
             gprop='')

    except requests.exceptions.Timeout:
        print("Timeout occured")


    data = pytrends.interest_over_time()
    return data

    # https://github.com/mdroste/stata-pylearn

if __name__ == "__main__":
    # getGoogleTrends(['unemployment'], 2011, 2019)
    # getGoogleTrends(['spider solitaire'], 2011, 2019)
    # getGoogleTrends(['pornhub'], 2011, 2019)
    # getGoogleTrends(['google flights'], 2011, 2019)
    # getGoogleTrends(['jobs near me'], 2011, 2019)
    # getGoogleTrends(['omegle'], 2011, 2019)
    # getGoogleTrends(['candy crush'], 2011, 2019)
    # getGoogleTrends(['linkedin'], 2011, 2019)
    # getGoogleTrends(['xbox'], 2011, 2019)
    # getGoogleTrends(['harvard'], 2011, 2019)
    # getGoogleTrends(['brownie recipe'], 2011, 2019)
    # getGoogleTrends(['blood drive'], 2011, 2019)
    # getGoogleTrends(['resume template'], 2011, 2019)
    # getGoogleTrends(['slutload'], 2011, 2019)
    # getGoogleTrends(['ebay'], 2011, 2019)
    # getGoogleTrends(['y combinator'], 2011, 2019)
    # getGoogleTrends(['calvin klein'], 2011, 2019)

    # getGoogleTrends(['vodka'], 2011, 2019)
    # getGoogleTrends(['jobs'], 2011, 2019)
    # getGoogleTrends(['haircut'], 2011, 2019)
    # getGoogleTrends(['lottery'], 2011, 2019)

    GTC.mergeAllSearch()











package linklist;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class CListTest {

    @Test
    void testConstructor() {
        CList<Integer> empty= new CList<>();
        assertEquals("[]", empty.toStringR());
        assertEquals("[]", empty.toString());
        assertEquals(0, empty.size());
    }

    @Test
    void testPrependAndToStringR() {

        CList<Integer> nums= new CList<>();
        nums.prepend(1);
        nums.prepend(2);
        nums.prepend(3);
        assertEquals("[1, 2, 3]", nums.toStringR());
//        assertEquals("[3, 2, 1]", nums.toString());
        assertEquals(3, nums.size());

        CList<Double> doub= new CList<>();
        doub.prepend(5.9);
        doub.prepend(4.9);
        doub.prepend(3.0);
        doub.prepend(8.9);
        assertEquals("[5.9, 4.9, 3.0, 8.9]", doub.toStringR());
//        assertEquals("[8.9, 3.0, 4.9, 5.9]", doub.toString());
        assertEquals(4, doub.size());

        CList<Character> ch= new CList<>();
        ch.prepend('b');
        ch.prepend('a');
        assertEquals("[b, a]", ch.toStringR());
//        assertEquals("[a, b]", ch.toString());
        assertEquals(2, ch.size());

    }

    @Test
    void testChangeHeadToNextAndAppend() {

        CList<Integer> empty= new CList<>();
        empty.append(1);
        assertEquals("[1]", empty.toStringR());
//        assertEquals("[1]", empty.toString());
        assertEquals(1, empty.size());

        CList<Character> some= new CList<>();
        some.append('a');
        some.append('b');
        some.append('c');
        some.append('d');
        assertEquals("[d, c, b, a]", some.toStringR());
//        assertEquals("[1]", empty.toString([a, b, c, d]));
        assertEquals(4, some.size());

        assertEquals('b', some.changeHeadToNext());
//      assertEquals("[1]", empty.toString([b, c, d, a]));
        assertEquals(4, some.size());

    }

}












    public String toStringR() { // Note:
        // TODO 1. In writing this, do NOT use fields size and head and the next fields.
        // Use only field tail and the prev and data fields.
        // Use the same scheme as in toString.

        // You can't test this fully until #2, prepend, is written.
        // Extreme case to watch out for: E is String and data items are the empty string.

        if (head == null) return "[]";
        StringBuilder sb= new StringBuilder("[");
        Node n= tail;

        while (n != head) {
            sb.append(n.data);
            sb.append(", ");
            n= n.prev;
        }
        sb.append(head.data + "]");
        return sb.toString();
    }

    /** Insert v at the beginning of the list. <br>
     * This operation takes constant time.<br>
     * E.g. if the list is [8, 7, 4], prepend(2) changes this list to [2, 8, 7, 4]. */
    public void prepend(E v) {
        // TODO 2. After writing this method, test this method and method
        // toStringR throughly before starting on the next method.
        // These two must be correct in order to be able to write and test all others.
        if (head == null) {
            head= new Node(null, v, null);
            tail= head;
        } else {
            Node n= new Node(head.prev, v, head);
            head.prev= n;
            head= n;
        }
        size+= 1;
    }

    /** Change the head of this list to head.next and return the new head.<br>
     * Thus, the head becomes the tail.<br>
     * E.g. if the list is [] or [5], the list is unchanged.<br>
     * E.g. With this list is [5, 3, 4, 6], calling the method <br>
     * .... changes the list to [3, 4, 6, 5]. <br>
     * This method takes constant time. */
    public Node changeHeadToNext() {
        // TODO 3.
        if (size < 2) { return head; }

        head= head.next;
//        tail= head;

        return head;

    }

    /** Add v to the end of this list. <br>
     * This operation takes constant time.<br>
     * E.g. if the list is [8, 7, 4], append(2) changes this list to [8, 7, 4, 2]. <br>
     * E.g. if the list is ["AB"], append(null) changes the list to ["AB", null]. */
    public void append(E v) {
        // TODO 4. After writing writing this method, test it thoroughly before
        // moving on to the next one.

        if (head == null) {
            head= new Node(head, v, tail);
            tail= head;
        } else {
            Node n= new Node(null, v, null);
            head.prev= n;
            n.next= head;
            n.prev= tail;
            tail= n;
        }
        size+= 1;

    }

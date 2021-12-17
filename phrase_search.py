import sys
sys.path.append('./classes/')
from utils import read_term_postings_fromdisk

def get_doc_id(posting, ptr):
        return posting[ptr].doc_id

def get_position(posting, ptr):
        return posting[ptr].term_positions
    
def intersect_postings(posting1,posting2,k):
        result = []                                                                     
        len1 = len(posting1)
        len2 = len(posting2)
        i = j = 0 
        while i != len1 and j != len2:                                                 
                if get_doc_id(posting1, i) == get_doc_id(posting2, j):
                        positions = []                                                          
                        pp1 = get_position(posting1, i)                                           
                        pp2 = get_position(posting2, j)                                           
                        plen1 = len(pp1)
                        plen2 = len(pp2)
                        pi = pj = 0 
                        while pi != plen1:                                              
                                while pj != plen2:                                      
                                        if abs(pp1[pi] - pp2[pj]) <= k:                 
                                                positions.append(pp2[pj])                       
                                        elif pp2[pj] > pp1[pi]:                        
                                                break    
                                        pj+=1                                                                                              
                                while positions != [] and abs(positions[0] - pp1[pi]) > k :             
                                        positions.remove(positions[0])                                  
                                for ps in positions:                                            
                                        result.append([ get_doc_id(posting1, i), pp1[pi], ps])    
                                pi+=1                                                   
                        i+=1                                                            
                        j+=1                                                            
                elif get_doc_id(posting1, i) < get_doc_id(posting2, j):                                      
                        i+=1                                                                                                                   
                else:
                        j+=1                                                            
        return result

def phrase_query_search(processed_query):
    terms_postings = {}
    result = []
    for word in processed_query:
        terms_postings[word] = read_term_postings_fromdisk(word)
    ptr_1 = 0
    ptr_2 = 1
    while ptr_1 < len(processed_query) and ptr_2 < len(processed_query):
        posting1 = terms_postings[processed_query[ptr_1]]
        posting2 = terms_postings[processed_query[ptr_2]]
        result = intersect_postings(posting1, posting2, 1)
        ptr_1 += 1
        ptr_2 += 1
    return result


        


    
            
    
    
    







        
        


    
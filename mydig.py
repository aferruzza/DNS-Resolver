import dns
import dns.message
import dns.query
import dns.rcode
import dns.name
import time

__author__ = "Andrew Ferruzza, ID: 111616974"

# Root servers derived from https://www.iana.org/domains/root/servers
global rootservers
rootservers = ['198.41.0.4', '192.228.79.201', '192.33.4.12', '199.7.91.13',
               '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53',
               '192.36.148.17', '192.58.128.30', '193.0.14.129', '199.7.83.42',
               '202.12.27.33']


# Helper method for question section
def print_question_section(domain_name):
    print("QUESTION SECTION:")
    print(domain_name, "IN A")


# Updates the size of the root servers after adding valid IPs. Increases speed of resolver
def update_servers(arr_of_servers, cut):
    size = len(arr_of_servers)
    trimmer_val = size - cut
    for i in arr_of_servers[0:trimmer_val]:
        arr_of_servers.remove(i)


def check_ip(ip_val):
    if ip_val.__contains__('.'):
        return True
    else:
        return False


def my_resolver(inp_domain, servers):
    """

    :param inp_domain: Takes in the domain that the user enters
    :param servers: Calls the root servers IP
    :return: prints out the response from the query sent and received to/from the domain entered
    The additional section of the response will return a list of IPs that can be split from the other
    information given in this section
    These IPs are then appended to the root server array, and parsed through for responses
    If responses are found "IN A", they are printed out with respective TTLs and IP addresses
    This method does NOT resolve CNAME (for bonus points), some domains will simply print the CNAME only

    """

    # Init the functions print value and servers list
    ans = "~~~DOMAIN COULD NOT BE RESOLVED~~~"
    ip_arr = servers

    # First, take in the domain and make a query with desired rdtype A, Internet class
    dname = dns.name.from_text(str(inp_domain))
    q = dns.message.make_query(dname, dns.rdatatype.A, dns.rdataclass.IN)
    try:
        for i in servers:
            # Handle cases like 'google.co.jp'
            if servers != '8.8.8.8':
                i = str(i)
                r = dns.query.udp(q, i, timeout=5)
            else:
                r = dns.query.udp(q, '8.8.8.8', timeout=5)

            # Parse required sections of the response
            additional = r.additional
            answer = r.answer
            # print(additional)

            # Loop through add. section and grab the last value of given str for the IP addresses
            for a in additional:
                # IPs are last value of the response in additional section lines
                ip_list = str(a).split()[-1]
                # print(ip_list)

                # Now pull just valid IP addresses => #.#.#.# format (IPv4)
                # Add IPs to IP list and update that list for faster results
                if check_ip(ip_list):
                    ip_arr.append(ip_list)
                    update_servers(ip_arr, 4)

            # Return answer section when non-zero ONLY
            if len(answer) != 0:
                for response in answer:
                    ans = response

        # Print the response from answer. Prints "Couldn't find domain" for domains not found
        # Recursive resolve for initial failures
        if servers != '8.8.8.8' and ans == "~~~DOMAIN COULD NOT BE RESOLVED~~~":
            my_resolver(inp_domain, '8.8.8.8')
        else:
            print(ans)

    # Handle exceptions for domains that throw exception
    except dns.exception.Timeout:
        print("Timeout. Try Again Please")
    except dns.exception.UnexpectedEnd:
        print("UNEXPECTED END. TRY AGAIN")


# Take user input and make sure user uses the 'mydig' command.
flag = True
while flag:
    while True:
        try:
            entry = str(input("Enter a domain name using 'mydig' or 'end' to end the program:"))
            if entry == "end":
                flag = False
                exit()
            sub_entry = "mydig"
            entry.index(sub_entry)
        except ValueError:
            print("Input must begin with 'mydig' command")
        else:
            break
    # Shorten input to just the domain
    domain_first = entry[6:]
    domain = domain_first.replace(' ', '')

    # print(domain)
    # Question section
    print_question_section(domain_first)
    print("\n")

    # Set var for the resolver stat
    resolver_start_time = time.time()


    def query_time():
        d = (time.time() - resolver_start_time) * 1000
        print("Query Time: ", "%.2f" % d, "milliseconds")


    def query_datetime():
        print("When: ", str(time.ctime()))


    # Answer section
    print("ANSWER SECTION:")
    my_resolver(domain, rootservers)
    print("\n")
    query_time()
    query_datetime()

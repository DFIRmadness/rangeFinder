# Range Finder
A python script that determines the range to a target based on Round Trip Times from traceroute.
The calculations are simple and not very accurate.  Some random source stated that the MAXIMUM distance was 100 KM per 1 ms RTT (Assuming terrestial lines).  Another source stated that there should be 1 ms subtracted for equipment lag. The calculated distances are so far off that it need to be cut in half so that RTT essentially becomes straight line.
True Purpose of this script is not to actually determine ranges (Note it is MAX range).  It was more for me to stretch the Python brain for a bit.

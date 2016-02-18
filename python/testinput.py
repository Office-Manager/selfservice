import sys

input = sys.argv[1]
print "the entire input of that string is %s" % input
print type(input)
print "about to try and split lines"
print "<br>"
lines = input.splitlines()
for file in lines:
	
	print file
	print "split line"
	print "<br>"
	

print "about to try and split on space"
print "<br>"
space = input.split(" ")
for file in space:
	print file
	print "split space"
	print "<br>"

	
#!/usr/bin/perl

print "#!/usr/bin/python\n\n";
print "def bgo_schema_str():\n";
print "\treturn \"\"\"\n";
foreach (<>) {
	print;
}
print "\t\"\"\"\n";

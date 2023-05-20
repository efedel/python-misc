#!/usr/bin/perl

print "#!/usr/bin/python\n\n";
print "def bgo_schema_str():\n";
print "\treturn \"\"\"\n";
foreach (<>) {
	$line = $_;
	$line =~ s/serial\tPRIMARY KEY/INTEGER PRIMARY KEY/;
	$line =~ s/bigint/INTEGER/;
	$line =~ s/bytea/BLOB/;
	$line =~ s/DEFAULT now\(\)/DEFAULT CURRENT_TIMESTAMP/;

	print $line;
}
print "\t\"\"\"\n";

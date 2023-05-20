-- BASTARD Database Schema


-- COMMENT:	Arbitrary text attached to a project, file, section,
--		instruction, etc. The notion of the 'next' field here
--		is that multiple comments can be attached to a single
--		location using a linked-list mechanism: each comment
--		refers to a followup comment in its next field, so that 
--		only a single comment ID is needed at a location to link
--		to a series of comments.
create table comment (
	id		number,		-- ID from sequence
	next		number,		-- ID of "next" comment
	repeat		number,		-- Make repeatable? (IDA users :P)
	text		varchar(512),
	primary key(id)
);

-- USER:	Someone who can access the DB. This can probably be farmed
--		out to the DB server itself.
create table user (
	id		number,		-- ID from sequence
	name		varchar(64),	-- username
	email		varchar(64),	-- email address
	im		varchar(64),	-- instant message service, ID
	primary key (id)
);

-- PROJECT:	The 'target'. It can include any number of related files.
create table project (			
	id		number,		-- unique ID from sequence
	name		varchar(20),	-- name of project
	create_date	date,		-- date project was created
	create_user	number,		-- who created it
	mod_date	date,		-- date project was last modified
	mod_user	number,		-- who modified it
	access_date	date,		-- date project was last accessed
	access_user	number,		-- who accessed it
	comment		number,		-- description of project
	primary key (id),
	foreign key (comment) references comment,
	foreign key (create_user) references user,
	foreign key (mod_user) references user

);

-- FILEIMAGE:	The location of a binary image of the file. This will be used
--		to obtain sequences of bytes (e.g. sections) to disassemble
--		on local or remote machines.
create table fileimage (
	id		number,		-- unique ID from sequence
	host		varchar(256),	-- IP/hostname where file resides
	name		varchar(256),	-- name of image file on host
	md5sum		varchar(256),
	primary key (id)
);

-- FILETYPE:	Valid values for the file.type field. These simply provide
--		hints for initial scanning/analysis.
create table filetype (
	id		number,
	name		varchar(64),
	primary key (id)
);

-- standalone executable
insert into filetype values( 1, 'Executable' );
-- dynamic/shared library
insert into filetype values( 2, 'Shared Library' );
-- static library
insert into filetype values( 3, 'Static Library' );
-- relocatable/linkable object code
insert into filetype values( 4, 'Linkable Object' );
-- archive of arbitrary files
insert into filetype values( 5, 'Archive' );
-- arbitrary data
insert into filetype values( 6, 'Data' );
	

-- OS_MODULE:	Valid values for the file.os field. These will have scanner
--		modules that perform OS-specific analysis on code and
--		data sections.
create table os_module (
	id		number,
	name		varchar(256),
	primary key (id)
);

insert into os_module values( 1, 'Linux' );
insert into os_module values( 2, 'FreeBSD' );
insert into os_module values( 3, 'OpenBSD' );
insert into os_module values( 4, 'NetBSD' );
insert into os_module values( 5, 'Solaris' );
insert into os_module values( 6, 'OSX' );
insert into os_module values( 7, 'DOS' );
insert into os_module values( 8, 'Win16' );
insert into os_module values( 9, 'Win9x' );
insert into os_module values( 10, 'WinNT' );

-- FILE:	A file within the project. A file may be a disassembly
--		target, complete with binary image, or a file referenced
--		by such a target (e.g. a shared library). A file may contain
--		other files, such as a tar file or an AR archive.
create table file (
	id		number,		-- unique ID from sequence
	project		number,		-- project owning this file
	name		varchar(256),	-- name of this file
	path		varchar(1024),	-- location of file relative to project
	type		number,		-- file type (exe, data, etc)
	format		varchar(64),	-- file format (ELF, PE, etc)
	os		varchar(64),	-- OS for file (Linux, FreeBSD, etc)
	container	number,		-- ID of file containing this one (ar)
	image		number,		-- ID of binary image for this file
	size		number,		-- Size of file in bytes
	create_date	date,		-- Date file entry was created
	create_user	number,		-- Who created it
	mod_date	date,		-- Date this file entry was modified
	mod_user	number,		-- Who modified it
	comment		number,		-- Description of file
	default_patch	number,		-- Default patchlevel (TODO)
	primary key (id),
	foreign key (project) references project,
	foreign key (type) references filetype,
	foreign key (os) references os_module,
	foreign key (image) references fileimage,
	foreign key (create_user) references user,
	foreign key (mod_user) references user,
	foreign key (comment) references comment,
	foreign key (default_patch) references patchlevel
);

-- PATCHLEVEL:	A patchlevel groups PATCH entries into logical clusters,
--		i.e. related changes made to a file image.
create table patchlevel (
	id		number,		-- unique ID from sequence
	name		varchar(128),	-- name of this patch-level
	file		number,		-- file patch is applied to
	create_date	date,		-- date patchlevel was created
	create_user	number,		-- who created it
	mod_date	date,		-- date patchlevel was last modified
	mod_user	number,		-- who modified it
	previous	number,		-- ID of patchlevel this was applied to
	comment		number,
	primary key (id),
	foreign key (file) references file,
	foreign key (create_user) references user,
	foreign key (mod_user) references user,
	foreign key (comment) references comment
);

-- PATCH:	A change made to the binary file image. Such changes are stored
--		in the DB and not in the file image, so that changes can be
--		rolled back, and arbitrary patched versions of the binary be
--		generated. The size of the patch is limited; multiple PATCH
--		entries are used to handle large patches. PATCH entries can
--		also be used to handle changes made by self-modifying code,
--		since each (disassembled) INSTRUCTION table entry will be
--		associated with a PATCHLEVEL. When performing disassembly,
--		a PATCHLEVEL is specified (default is file.default_patch), and
--		any binary patches for that PATCHLEVEL are applied to the
--		bytestream before it is sent to the disassembler.
create table patch (
	id		number,		-- unique ID from sequence
	patchlevel	number,		-- ID of patchlevel owning this patch
	offset		number,		-- offset in file to apply patch
	length		number,		-- number of bytes to patch
	bytes		varchar(64),	-- bytes to patch with
	comment		number,
	primary key (id),
	foreign key (patchlevel) references patchlevel,
	foreign key (comment) references comment
);


-- SECTIONTYPE:	Valid values for the section.type field. These are used to
--		provide hints to analysis engines, e.g. whether to 
--		disassemble a section or not.
create table sectiontype (
	id		number,
	name		varchar(64),
	primary key (id)
);

insert into sectiontype values (1, 'code');
insert into sectiontype values (2, 'data');
insert into sectiontype values (3, 'debug');
insert into sectiontype values (4, 'header');
insert into sectiontype values (5, 'string');
insert into sectiontype values (6, 'resource');

-- ARCH_MODULE:	Valid values for the section.arch field. These have scanner
--		modules that perform architecture-specific analysis (such
--		as disassembly) on code and data sections.
create table arch_module (
	id		number,
	name		varchar(64),
	endian		char(16),	-- 'little' or 'big'
	sz_word		number,		-- size of a machine word in bytes
	sz_address	number,		-- size of an address n bytes
	primary key (id)
);

insert into arch_module values( 1, 'x86', 'little', 4, 4 );
insert into arch_module values( 2, 'x86-64', 'little', 8, 8 );
insert into arch_module values( 3, 'ia64', 'little', 8, 8 );
insert into arch_module values( 4, 'SPARC', 'big', 8, 8 );


-- COMPILER_MODULE:	Valid values for the section.compiler field. These
--			have scanner modules which perform compiler-specific
--			analysis on code and data sections.
create table compiler_module (
	id		number,
	name		varchar(256),
	primary key (id)
);

insert into compiler_module values ( 1, "gcc" );
insert into compiler_module values ( 2, "Sun CC" );
insert into compiler_module values ( 3, "Visual C++" );

-- SOURCE_MODULE:	Valid values for the section.source field. These have
--			scanner modules which perform source-specific analysis
--			on code and data sections.
create table source_module (
	id		number,
	name		varchar(256),
	primary key (id)
);

insert into source_module values( 1, 'C' );
insert into source_module values( 2, 'FORTRAN' );
insert into source_module values( 3, 'JAVA' );


-- SECTION:	A section within the file.
create table section (
	id		number,		-- unique ID from sequence
	name		varchar(64),	-- name of section
	type		number,		-- type of section (code, data, etc)
	file		number,		-- ID of file containing section
	offset		number,		-- offset into file of section start
	size		number,		-- size of section in bytes
	address		number,		-- load address (rva) of section
	arch		varchar(64),	-- CPU Architecture
	compiler	varchar(64),	-- Compiler used on section
	source		varchar(64),	-- Source code language
	comment		number,		-- description of section
	primary key (id),
	foreign key (type) references sectiontype,
	foreign key (file) references file,
	foreign key (arch) references arch_module,
	foreign key (compiler) references compiler_module,
	foreign key (source) references souce_module,
	foreign key (comment) references comment
);

-- BASETYPE:
create table basetype(
	id		number,		-- unique ID from sequence
	name		varchar(64),	-- name of base type
	primary key (id)
);

-- BASETYPE TABLE DATA:
--	TODO : use more sophisticated types, e.g.
-- 	scalar logical, scalar char, calar string, scalar int, 
-- 	scalar rational, scalar real, scalar complex
-- 	container/record, array, ref/pointer, set, list, file, stream
-- scalar/int type
insert into basetype values (1, 'scalar');
-- address/pointer type
insert into basetype values (2, 'reference');
-- aggregate/struct type
insert into basetype values (3, 'container');
insert into basetype values (4, 'union');


-- DATATYPE:
-- TODO: handle bit-sized datatypes
create table datatype (
	id		number,		-- unique ID from sequence
	name		varchar(256),	-- name of type
	basetype	number,		-- ID of BASETYPE
	size		number,		-- size in bytes
	align		number,		-- Alignment
	parent		number,		-- ID of DATATYPE container
	primary key (id),
	foreign key (basetype) references basetype
);

-- SYMSCOPE:
create table symscope (
	id		number,
	name		varchar(32),
	primary key (id)
);

-- global to project
insert into symscope values (1, 'global');
-- local to file
insert into symscope values (2, 'file');
-- local to codeblock
insert into symscope values (3, 'block');

-- SYMTYPE:
create table symtype (
	id		number,
	name		varchar(64),
	primary key (id)
);

-- code label includes function names
insert into symtype values ( 1, 'code label' );
insert into symtype values ( 2, 'string' );
insert into symtype values ( 3, 'variable' );
insert into symtype values ( 4, 'import' );
insert into symtype values ( 5, 'source code line' );

-- SYMBOL:
create table symbol (
	id		number,
	name		varchar(256),	-- name of symbol
	type		number,		-- type of symbol
	scope		number,		-- scope of symbol
	primary key (id),
	foreign key (type) references symtype,
	foreign key (scope) references symscope
);

-- INSN_DEF: 	Definition of a CPU instruction. These are shared among 
-- 		INSTRUCTION table entries; they can be considered
--		instruction types.
create table insn_def (
	id		number,		-- unique ID from sequence
	class		number,		-- instruction group
	type		number,		-- instruction type
	mnemonic	varchar(16),	-- duh
	flags_set	number,		-- flags that are modified
	flags_test	number,		-- flags that are tested

	primary key (id)
);

-- INSTRUCTION:	An instance of an INSN_DEF; a completeley disassembled
--		instruction.
create table instruction (
	id		number,		-- unique ID from sequence
	section		number,		-- section owning this insn
	offset		number,		-- offset (from section start ?)
	address		number,		-- load address of section
	insn_def	number,		-- INSN_DEF for this insn
	patch		number,		-- PATCHLEVEL owning this insn
	comment		number,		-- Comment :)
	primary key (id),
	foreign key (section) references section,
	foreign key (insn_def) references insn_def,
	foreign key (patch) references patchlevel,
	foreign key (comment) references comment
);

-- OP_DEF:	Operand definition. Like INSN_DEF, these are 'types' of
--		operands which are referenced by the OPERAND table entries.
create table op_def (
	id		number,		-- unique ID from sequence
	name		varchar(8),	-- name of operand (dest, src1, src2)
	type		number,		-- Operand type
	value		number,		-- Immediate value, regiser ID, etc
	access		number,		-- RWX
	size		number,		-- Size of operand in bytes
--	insn_def	number,		-- associate with INSN_DEF??
--	datatype	number,		-- assocate with a data type??
--	offset		number,		-- offset from start of insn ??
	primary key (id)
);

-- OPERAND:	An instance of an OP_DEF.
create table operand (
	id		number,		-- unique ID from sequence
	insn		number,		-- INSTRUCTION owning this operand
	op_def		number,		-- OP_DEF for this operand
	symbol		number,		-- Symbolic name for operand contents
	comment		number,		-- 
	primary key (id),
	foreign key (insn) references instruction,
	foreign key (op_def) references op_def,
	foreign key (symbol) references symbol,
	foreign key (comment) references comment
);

-- CODEBLOCK
create table codeblock (
	id		number,		-- unique ID from sequence
	parent		number,		-- ID of CODEBLOCK containing this one
	start		number,		-- start INSTRUCTION
	end		number,		-- end INSTRUCTION
	comment		number,		--
	primary key (id),
	foreign key (start) references instruction,
	foreign key (end) references instruction,
	foreign key (comment) references comment
);

-- FUNCTION
create table function (
	id		number,		-- unique ID from sequence
	primary key (id)
);

-- CODEREF
create table coderef (
	id		number,		-- unique ID from sequence
	primary key (id)
);

-- DATAREF
create table dataref (
	id		number,		-- unique ID from sequence
	primary key (id)
);

-- FUNCREF
create table funcref (
	id		number,		-- unique ID from sequence
	primary key (id)
);

-- FILEREF
create table fileref (
	id		number,		-- unique ID from sequence
	primary key (id)
);

-- DATA
create table data (
	id		number,		-- unique ID from sequence
	primary key (id)
);

-- CODEMACRO
create table codemacro (
	id		number,		-- unique ID from sequence
	primary key (id)
);


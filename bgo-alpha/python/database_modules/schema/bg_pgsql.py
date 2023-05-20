#!/usr/bin/python

def bgo_schema_str():
	return """
-- Big O Database Schema
-- NOTE: This schema contains Postgres-specific data types such as 
-- serial	PRIMARY KEY and bytea to implement autoincrementing types 
-- and BLOBs. The rest should be standard SQL.
--
-- IMPORTANT: do not use semicolons except as end-of-command delimiters. 
--            this file is split on semicolons when processed by Sqlite!

-- =========================================================================
--                        Big O Database MetaInfo
-- =========================================================================

CREATE TABLE bgo_module (
	id		serial	PRIMARY KEY,
	name		varchar(256),
	version		float		DEFAULT 1.0,
	create_date	timestamp	DEFAULT now(),
	author		varchar(256)	DEFAULT 'Nobody',
	license		varchar(245)	DEFAULT 'LGPL'
);

CREATE INDEX bgo_module_name_idx ON bgo_module(name);

INSERT INTO bgo_module (name, version, author, license) 
VALUES ('bgo', 0.2, 'mammon_', 'LGPL');

-- MODULE_CLASS:	Associates a FILE or INSN_DEF row with the class and
--			module used to create it. This is needed to restore 
--			module-specific objects from the DB.
--			Any class registered here will be instantiated
--			by dbobject.BuildModuleClass(), which passes only
--			a db_id to the class __init__().
CREATE TABLE module_class (
	id		serial	PRIMARY KEY,		
	module		integer REFERENCES bgo_modules(id),
	-- name of file containing class
	filename	varchar(64),
	-- name of class
	classname	varchar(64)
);

-- CREATE INDEX module_class_name_idx ON module_class(classname);
-- CREATE INDEX module_class_name_idx ON module_class(filename);

-- Built-in BGO module classes:
-- Instructon: Arithmetic
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'Add'); 	-- 1
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'Sub'); 	-- 2
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'Mul'); 	-- 3
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'Div'); 	-- 4
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'ShiftLeft'); 	-- 5
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'ShiftRight'); 	-- 6
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'AbsoluteVal');	-- 7
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'SquareRoot'); 	-- 8
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'Tangent'); 	-- 9
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'Sine'); 	-- 10
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Arithmetic', 'Cosine'); 	-- 11
-- Instructon: Bit
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Bit', 'Set'); 		-- 12
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Bit', 'Clear'); 		-- 13
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Bit', 'Toggle'); 		-- 14
-- Instructon: Compare
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Compare', 'Compare');	-- 15
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Compare', 'Test'); 		-- 16
-- Instructon: ControlFlow
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.ControlFlow', 'BranchCond');	-- 17
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.ControlFlow', 'BranchAlways'); -- 18
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.ControlFlow', 'CallCond'); 	-- 19
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.ControlFlow', 'CallAlways'); -- 20
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.ControlFlow', 'Return'); 	-- 21
-- Instructon: LoadStore
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.LoadStore', 'Move'); 	-- 22
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.LoadStore', 'MoveCond'); 	-- 23
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.LoadStore', 'Exchange'); 	-- 24
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.LoadStore', 'ExchangeCond'); -- 25
-- Instructon: Logic
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Logic', 'And'); 		-- 26
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Logic', 'Or'); 		-- 27
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Logic', 'Xor'); 		-- 28
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Logic', 'Not'); 		-- 29
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Logic', 'Neg'); 		-- 30
-- Instructon: Misc
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Misc', 'Nop'); 		-- 31
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Misc', 'Unknown'); 		-- 32
-- Instructon: Stack
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Stack', 'Push'); 		-- 33
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Stack', 'Pop'); 		-- 34
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Stack', 'PushRegisters'); 	-- 35
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Stack', 'PopRegisters'); 	-- 36
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Stack', 'PushFlags'); 	-- 37
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Stack', 'PopFlags'); 	-- 38
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Stack', 'EnterFrame');	-- 39
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Stack', 'LeaveFrame'); 	-- 40
-- Instructon: System
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.System', 'IOPortRead'); 	-- 41
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.System', 'IOPortWrite'); 	-- 42
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.System', 'CpuID'); 		-- 43
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.System', 'Halt'); 		-- 44
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.System', 'SysCtl'); 		-- 45
-- Instructon: Trap
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Trap', 'Trap'); 		-- 46
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Trap', 'TrapCond'); 		-- 47
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Trap', 'TrapReturn'); 	-- 48
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Trap', 'Bound'); 		-- 49
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Trap', 'Debug'); 		-- 50
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Trap', 'Trace'); 		-- 51
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Trap', 'InvalidOpcode'); 	-- 52
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGInstructions.Trap', 'Overflow'); 		-- 53
-- File: BGFile
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGFile', 'File');				-- 54
-- File: BGObjFile
INSERT INTO module_class (module, filename, classname) 
	VALUES (1, 'BGObjFile', 'ObjFile');			-- 55

-- =========================================================================
--                           Projects and Files
-- =========================================================================

-- PROJECT:	The 'target'. It can include any number of related files.
CREATE TABLE project (			
	id		serial	PRIMARY KEY,
	name		varchar(64),	-- name of project
	version		float,		-- just in case
	create_date	timestamp 	DEFAULT now(),
	mod_date	timestamp	-- date project was last modified
);

CREATE INDEX project_name_idx ON project(name);

-- LAYER : A layer of bytes and the resulting code/data. This is intended
--         to be used by an IDE or analysis program, not modified 
--         directly by the user. The intent is to support multiple 
--         representations of the file, which is useful for packed
--         files, self-modifying code, overlays, and so forth.
CREATE TABLE layer (
	id		serial	PRIMARY KEY,
	name		varchar(64),
	parent		integer references layer(id)
);

-- CREATE INDEX layer_name_idx ON layer(name);
-- CREATE INDEX layer_parent_idx ON layer(parent);


-- FILEIMAGE:	The location of a binary image of the file. This will be used
--		to obtain sequences of bytes (e.g. sections) to disassemble
--		on local or remote machines.
CREATE TABLE file_image (
	id		serial	PRIMARY KEY,
	host		varchar(256),	-- IP/hostname where file resides
	name		varchar(256),	-- name of image file on host
	md5sum		varchar(256),
	image		bytea		-- binary image in db
);

-- CREATE INDEX file_image_host_idx ON file_image(host);
-- CREATE INDEX file_image_name_idx ON file_image(name);
-- CREATE INDEX file_image_md5_idx ON file_image(md5sum);

-- FILE_TYPE:	Valid values for the file.type field.
CREATE TABLE file_type (
	id		integer PRIMARY KEY,
	name		varchar(64)
);

INSERT INTO file_type (id, name) VALUES ( 1, 'unknown' );
-- standalone executable
INSERT INTO file_type (id, name) VALUES ( 2, 'executable' );
-- dynamic/shared library
INSERT INTO file_type (id, name) VALUES ( 3, 'shared library' );
-- static library
INSERT INTO file_type (id, name) VALUES ( 4, 'static library' );
-- relocatable/linkable object code
INSERT INTO file_type (id, name) VALUES ( 5, 'linkable object' );
-- arbitrary data
INSERT INTO file_type (id, name) VALUES ( 6, 'data' );
	

-- FILE_FORMAT:	Valid values for the file.format column.
CREATE TABLE file_format (
	id		integer PRIMARY KEY,
	name		varchar(64)
);

INSERT INTO file_format (id, name) VALUES ( 1, 'unknown' );
INSERT INTO file_format (id, name) VALUES ( 2, 'ELF' );
INSERT INTO file_format (id, name) VALUES ( 3, 'AR' );
INSERT INTO file_format (id, name) VALUES ( 4, 'AOUT' );
INSERT INTO file_format (id, name) VALUES ( 5, 'OMF' );
INSERT INTO file_format (id, name) VALUES ( 6, 'MZ' );
INSERT INTO file_format (id, name) VALUES ( 7, 'PE' );

-- FILE_OS:	Valid values for the file.os column.
CREATE TABLE file_os (
	id		integer PRIMARY KEY,
	name		varchar(64)
);

INSERT INTO file_os (id, name) VALUES ( 1, 'Unknown' );
INSERT INTO file_os (id, name) VALUES ( 2, 'Linux' );
INSERT INTO file_os (id, name) VALUES ( 3, 'FreeBSD' );
INSERT INTO file_os (id, name) VALUES ( 4, 'OpenBSD' );
INSERT INTO file_os (id, name) VALUES ( 5, 'NetBSD' );
INSERT INTO file_os (id, name) VALUES ( 6, 'Solaris' );
INSERT INTO file_os (id, name) VALUES ( 7, 'OS/X' );
INSERT INTO file_os (id, name) VALUES ( 8, 'DOS' );
INSERT INTO file_os (id, name) VALUES ( 9, 'Win16' );
INSERT INTO file_os (id, name) VALUES ( 10, 'Win9x' );
INSERT INTO file_os (id, name) VALUES ( 11, 'WinNT/2K/XP' );

-- ARCH : Architecture for file contents
CREATE TABLE arch (
	id		integer PRIMARY KEY,
	name		varchar(16),
	endian		char(8),	-- 'little' or 'big'
	sz_word		integer,	-- size of a machine word in bytes
	sz_addr		integer		-- size of an address n bytes
);

INSERT INTO arch (id, name, endian, sz_word, sz_addr) 
VALUES ( 1, 'Unknown', 'little', 4, 4 );
INSERT INTO arch (id, name, endian, sz_word, sz_addr) 
VALUES ( 2, 'x86', 'little', 4, 4 );
INSERT INTO arch (id, name, endian, sz_word, sz_addr) 
VALUES ( 3, 'x86-64', 'little', 8, 8 );
INSERT INTO arch (id, name, endian, sz_word, sz_addr) 
VALUES ( 4, 'SPARC', 'big', 8, 8 );
INSERT INTO arch (id, name, endian, sz_word, sz_addr) 
VALUES ( 5, 'PPC', 'big', 8, 8 );
INSERT INTO arch (id, name, endian, sz_word, sz_addr) 
VALUES ( 6, 'ARM', 'little', 4, 4 );
INSERT INTO arch (id, name, endian, sz_word, sz_addr) 
VALUES ( 7, 'JVM', 'big', 4, 4 );
INSERT INTO arch (id, name, endian, sz_word, sz_addr) 
VALUES ( 8, 'CLR', 'little', 4, 4 );
INSERT INTO arch (id, name, endian, sz_word, sz_addr) 
VALUES ( 9, 'IA64', 'little', 8, 8 );

-- FILE:	A file within the project. A file may be a disassembly
--		target, complete with binary image, or a file referenced
--		by such a target (e.g. a shared library). A file may contain
--		other files, such as a tar file or an AR archive.
CREATE TABLE file (
	id		serial	PRIMARY KEY,
	name		varchar(256),	-- name of this file
	path		varchar(1024),	-- location of file relative to project
	ident		varchar(128),	-- results of magic
	type		integer REFERENCES file_type(id)	DEFAULT 1,
	format		integer REFERENCES file_format(id)	DEFAULT 1,
	os		integer REFERENCES file_os(id)		DEFAULT 1,	
	arch		integer REFERENCES arch(id)		DEFAULT 1,
	-- BGO Class and Disassembler Module name
	class		integer REFERENCES module_class(id),
	-- container is the id of the file (if any) containing this file
	container	integer REFERENCES file(id)		DEFAULT NULL,
	image		integer REFERENCES file_image(id),
	size		bigint,	
	version		float,		-- for user use
	create_date	timestamp	DEFAULT now(),
	mod_date	timestamp	-- Date this file entry was modified
);

CREATE INDEX file_name_idx ON file(name);
CREATE INDEX file_path_idx ON file(path);
--CREATE INDEX file_type_idx ON file(type);
--CREATE INDEX file_format_idx ON file(format);
--CREATE INDEX file_os_idx ON file(os);
--CREATE INDEX file_arch_idx ON file(arch);
--CREATE INDEX file_container_idx ON file(container);

-- PROJECT_FILE_MAP: associate files with a project
CREATE TABLE project_file_map (
	id		serial	PRIMARY KEY,
	project		integer REFERENCES project(id),
	file		integer REFERENCES file(id)
);

CREATE INDEX project_file_proj_map ON project_file_map(project);
CREATE INDEX project_file_file_map ON project_file_map(file);

-- FILE_LAYER_MAP : Associates layers with a file. File layers may be used
--                  to track file patches, or as disassembly layers when
--                  a process image is not being used.
CREATE TABLE file_layer_map (
	id		serial	PRIMARY KEY,
	file		integer REFERENCES file(id),
	layer		integer REFERENCES layer(id)
);

CREATE INDEX file_layer_map_file_idx ON file_layer_map(file);
CREATE INDEX file_layer_map_layer_idx ON file_layer_map(layer);

-- PATCH:	A change made to the binary file image. Such changes are stored
--		in the DB and not in the file image, so that changes can be
--		rolled back, and arbitrary patched versions of the binary be
--		generated. Note that each patch is a contiguous sequence of
--              bytes. Also note that a patch is for a file only. To 
--              modify memory (e.g. a process image), create a new memory
--              allocation at the address being modified in the current layer. 
CREATE TABLE patch (
	id		serial	PRIMARY KEY,
	file		integer REFERENCES file(id),
	revision	float,		-- version number of patch
	file_offset	bigint,		-- offset in file to apply patch
	length		integer,	-- number of bytes to patch
	bytes		bytea		-- bytes to patch with
);

CREATE INDEX patch_file_idx ON patch(file);
CREATE INDEX patch_offset_idx ON patch(file_offset);

-- LAYER_PATCH_MAP : Applying a patch to an image generates a new layer. Each
--                   layer after layer 0 is therefore composed of patches
--                   applied to previous layers. This table associates a
--                   layer with the patches that created it.
CREATE TABLE layer_patch_map (
	id		serial	PRIMARY KEY,
	layer		integer REFERENCES layer(id),
	patch		integer REFERENCES patch(id)
);

CREATE INDEX layer_patch_map_layer_idx ON layer_patch_map(layer);
CREATE INDEX layer_patch_map_patch_idx ON layer_patch_map(patch);


-- =========================================================================
--                           Process Image
-- =========================================================================
-- PROCESS_IMAGE : The runtime memory space of a program. Includes files,
--                 shared libraries, and memory allocations
CREATE TABLE process_image (
	id		serial PRIMARY KEY,
	create_date	timestamp	DEFAULT now()
);

-- PROCESS_LAYER_MAP : Associates layers with a process image. Process layers
--                     may be used to track memory allocations, writes to
--                     memory, or as disassembly layers (multiple 
--                     interpretations of the same code.
CREATE TABLE process_layer_map (
	id		serial	PRIMARY KEY,
	process		integer REFERENCES process_image(id),
	layer		integer REFERENCES layer(id)
);

CREATE INDEX process_layer_map_layer_map_idx ON process_layer_map(layer);
CREATE INDEX process_layer_map_proc_map_idx ON process_layer_map(process);

-- PROCESS_FILE_MAP : Represents a file mapped into memory, e.g. an 
--                    executable or shared library maped into a process
--                    image.
CREATE TABLE process_file_map (
	id		serial PRIMARY KEY,
	process		integer REFERENCES process_image(id),
	file		integer REFERENCES file(id),
	address		bigint		-- load address of file
);

CREATE INDEX process_file_map_file_map_idx ON process_file_map(file);
CREATE INDEX process_file_map_proc_map_idx ON process_file_map(process);
CREATE INDEX process_file_map_addr_map_idx ON process_file_map(address);

-- PROJECT_PROCESS_MAP: associate process images with a project
CREATE TABLE project_process_map (
	id		serial	PRIMARY KEY,
	project		integer REFERENCES project(id),
	process		integer REFERENCES process_image(id)
);

CREATE INDEX project_process_map_proj_map_idx ON project_process_map(project);
CREATE INDEX project_process_map_proc_map_idx ON project_process_map(process);

-- MEMORY_ALLOCATION : A block of memory that has been allocated but does
--                     not map explicitly to file. Examples are heap
--                     allocations, PSP prefix, .bss section.
CREATE TABLE memory_allocation (
	id		serial PRIMARY KEY,
	process		integer REFERENCES process_image(id),
	layer		integer REFERENCES layer(id),
	address		bigint,
	size		bigint,
	bytes		bytea
);

CREATE INDEX memory_alloc_process_idx ON memory_allocation(process);
CREATE INDEX memory_alloc_layer_idx ON memory_allocation(layer);
CREATE INDEX memory_alloc_address_idx ON memory_allocation(address);

-- =========================================================================
--                           File/Process Sections
-- =========================================================================

-- SECTIONTYPE:	Valid values for the section.type field. These are used to
--		provide hints to analysis engines, e.g. whether to 
--		disassemble a section or not.
CREATE TABLE section_type (
	id		integer PRIMARY KEY,
	name		varchar(64)
);

INSERT INTO section_type (id, name) VALUES (1, 'header');
INSERT INTO section_type (id, name) VALUES (2, 'code');
INSERT INTO section_type (id, name) VALUES (3, 'data');
INSERT INTO section_type (id, name) VALUES (4, 'resource');
INSERT INTO section_type (id, name) VALUES (5, 'debug');
INSERT INTO section_type (id, name) VALUES (6, 'symbol');
INSERT INTO section_type (id, name) VALUES (7, 'import');
INSERT INTO section_type (id, name) VALUES (8, 'export');
INSERT INTO section_type (id, name) VALUES (9, 'reloc');
INSERT INTO section_type (id, name) VALUES (10, 'note');


-- COMPILER: The compiler which generated code in a section
CREATE TABLE compiler (
	id		integer PRIMARY KEY,
	name		varchar(64)
);

INSERT INTO compiler (id, name) VALUES ( 1, 'Unknown' );
INSERT INTO compiler (id, name) VALUES ( 2, 'gcc' );
INSERT INTO compiler (id, name) VALUES ( 3, 'Sun CC' );
INSERT INTO compiler (id, name) VALUES ( 4, 'Visual C++' );

-- SOURCE_LANG: The high-level language a section was written in
CREATE TABLE source_lang (
	id		integer PRIMARY KEY,
	name		varchar(64)
);

INSERT INTO source_lang VALUES ( 1, 'Assembler' );
INSERT INTO source_lang VALUES ( 2, 'C' );
INSERT INTO source_lang VALUES ( 3, 'C++' );
INSERT INTO source_lang VALUES ( 4, 'C#' );
INSERT INTO source_lang VALUES ( 5, 'JAVA' );
INSERT INTO source_lang VALUES ( 6, 'FORTRAN' );


-- SECTION:	A section within the file.
create table section (
	id		serial	PRIMARY KEY,
	file		integer REFERENCES file(id),
	type		integer REFERENCES section_type(id)	DEFAULT 1,
	name		varchar(64),
	flags		varchar(64),
	access		integer,
	file_offset	bigint,
	load_addr	bigint,
	size		bigint,
	alloc_size	bigint,				-- in-memory size
	arch		integer REFERENCES arch(id)		DEFAULT 1,
	compiler	integer REFERENCES compiler(id)		DEFAULT 1,
	source		integer REFERENCES source_lang(id)	DEFAULT 1
);

CREATE INDEX section_name_idx ON section(name);
--CREATE INDEX section_access_idx ON section(access);
--CREATE INDEX section_offset_idx ON section(file_offset);
--CREATE INDEX section_address_idx ON section(load_addr);
--CREATE INDEX section_type_idx ON section(type);
--CREATE INDEX section_file_idx ON section(file);

-- PROCESS_SECTION_MAP : Associates a section with a process image
CREATE TABLE process_section_map (
	id		serial	PRIMARY KEY,
	process		integer REFERENCES process_image(id),
	section		integer REFERENCES section(id),
	address		bigint			-- load address of section
);

CREATE INDEX process_section_map_proc_idx ON process_section_map(process);
CREATE INDEX process_section_map_sec_idx ON process_section_map(section);
CREATE INDEX process_section_map_addr_idx ON process_section_map(address);

-- =========================================================================
--                           Data and Datatypes
-- =========================================================================

-- BASE_TYPE: Primitive data types, which user-defined datatypes are built from.
CREATE TABLE base_type(
	id		integer PRIMARY KEY,
	name		varchar(64)
);

-- BASETYPE TABLE DATA:
--	TODO : use more sophisticated types, e.g.
-- 	scalar logical, scalar char, scalar string, scalar int, 
-- 	scalar rational, scalar real, scalar complex
-- 	container/record, array, ref/pointer, set, list, file, stream
-- scalar/int type
INSERT INTO base_type (id, name) VALUES (1, 'scalar');
-- address/pointer type
INSERT INTO base_type (id, name) VALUES (2, 'reference');
-- aggregate/struct type
INSERT INTO base_type (id, name) VALUES (3, 'container');
INSERT INTO base_type (id, name) VALUES (4, 'union');


-- DATATYPE: Built-in and user-defined types.
-- TODO: handle bit-sized datatypes
--        NOTE: a pointer is conceptually an array of the datatype at
--              the dereferenced address. Thus all pointers are containers
--              of 1 or more elements of datatype, e.g.:
--              To create a pointer for a datatype named 'name' of base 
--              type 'basetype', size 'size', etc:
-- 		1. create datatype
--		  dtype_id = INSERT name, basetype, size, align, 0, 0 
--		2. create pointer to datatype
--		  ptr_id = INSERT name + ' *', 'reference', 4, 0, dtype_id, 0
--		...then use ptr_id for the address of the pointer itself
CREATE TABLE datatype (
	id		serial	PRIMARY KEY,
	name		varchar(256),	-- name of type
	basetype	integer REFERENCES base_type(id)	DEFAULT 1,
	size		integer,	-- size in bytes
	align		integer,	-- Alignment (1, 2, 4, 8...)
	-- datatype this is a reference to, if applicable
	reference	integer REFERENCES datatype(id)		DEFAULT NULL,
	-- datatype containing this, if applicable
	container	integer REFERENCES datatype(id)
);

CREATE INDEX datatype_name_map ON datatype(name);
--CREATE INDEX datatype_basetype_map ON datatype(basetype);

-- DATA : A data address. Has an associated data type. 
CREATE TABLE data (
	id		serial	PRIMARY KEY,
	file_offset	bigint,	-- offset (from file start)
	address		bigint,	-- load address
	datatype	integer REFERENCES datatype(id),
	count		integer		-- for arrays
);

--CREATE INDEX data_offset_idx ON data(file_offset);
CREATE INDEX data_addr_idx ON data(address);

-- LAYER_DATA_MAP : What happens with code, happens with data as well...
CREATE TABLE layer_data_map (
	id		serial	PRIMARY KEY,
	layer		integer REFERENCES layer(id),
	data		integer REFERENCES data(id)
);

CREATE INDEX layer_data_map_layer_idx ON layer_data_map(layer);
CREATE INDEX layer_data_map_data_idx ON layer_data_map(data);


-- =========================================================================
--                      Disassembled Instructions
-- =========================================================================

-- INSN_MAJOR_TYPE : the group or general type of an instruction
CREATE TABLE insn_major_type (
	id		integer PRIMARY KEY,
	name		varchar(20)
);

INSERT INTO insn_major_type(name) VALUES ('None');
INSERT INTO insn_major_type(name) VALUES ('Control Flow');
INSERT INTO insn_major_type(name) VALUES ('Arithmetic');
INSERT INTO insn_major_type(name) VALUES ('Logical');
INSERT INTO insn_major_type(name) VALUES ('Stack');
INSERT INTO insn_major_type(name) VALUES ('Compare');
INSERT INTO insn_major_type(name) VALUES ('Load/Store');
INSERT INTO insn_major_type(name) VALUES ('Bit');
INSERT INTO insn_major_type(name) VALUES ('Trap');
INSERT INTO insn_major_type(name) VALUES ('System');
INSERT INTO insn_major_type(name) VALUES ('Misc');

-- INSN_MINOR_TYPE : the specific type of an instruction
CREATE TABLE insn_minor_type (
	id		integer PRIMARY KEY,
	name		varchar(16)
);

INSERT INTO insn_minor_type (name) VALUES ('invalid');
INSERT INTO insn_minor_type (name) VALUES ('jump');
INSERT INTO insn_minor_type (name) VALUES ('cond jump');
INSERT INTO insn_minor_type (name) VALUES ('call');
INSERT INTO insn_minor_type (name) VALUES ('cond call');
INSERT INTO insn_minor_type (name) VALUES ('return');
INSERT INTO insn_minor_type (name) VALUES ('add');
INSERT INTO insn_minor_type (name) VALUES ('sub');
INSERT INTO insn_minor_type (name) VALUES ('mul');
INSERT INTO insn_minor_type (name) VALUES ('div');
INSERT INTO insn_minor_type (name) VALUES ('shiftl');
INSERT INTO insn_minor_type (name) VALUES ('shiftr');
INSERT INTO insn_minor_type (name) VALUES ('abs');
INSERT INTO insn_minor_type (name) VALUES ('sqrt');
INSERT INTO insn_minor_type (name) VALUES ('cos');
INSERT INTO insn_minor_type (name) VALUES ('tan');
INSERT INTO insn_minor_type (name) VALUES ('sine');
INSERT INTO insn_minor_type (name) VALUES ('and');
INSERT INTO insn_minor_type (name) VALUES ('or');
INSERT INTO insn_minor_type (name) VALUES ('xor');
INSERT INTO insn_minor_type (name) VALUES ('not');
INSERT INTO insn_minor_type (name) VALUES ('neg');
INSERT INTO insn_minor_type (name) VALUES ('push');
INSERT INTO insn_minor_type (name) VALUES ('pop');
INSERT INTO insn_minor_type (name) VALUES ('enter frame');
INSERT INTO insn_minor_type (name) VALUES ('leave frame');
INSERT INTO insn_minor_type (name) VALUES ('test');
INSERT INTO insn_minor_type (name) VALUES ('cmp');
INSERT INTO insn_minor_type (name) VALUES ('move');
INSERT INTO insn_minor_type (name) VALUES ('cond move');
INSERT INTO insn_minor_type (name) VALUES ('xchng');
INSERT INTO insn_minor_type (name) VALUES ('cond xchg');
INSERT INTO insn_minor_type (name) VALUES ('bclear');
INSERT INTO insn_minor_type (name) VALUES ('bset');
INSERT INTO insn_minor_type (name) VALUES ('btog');
INSERT INTO insn_minor_type (name) VALUES ('trap');
INSERT INTO insn_minor_type (name) VALUES ('cond trap');
INSERT INTO insn_minor_type (name) VALUES ('trap ret');
INSERT INTO insn_minor_type (name) VALUES ('bound trap');
INSERT INTO insn_minor_type (name) VALUES ('debug trap');
INSERT INTO insn_minor_type (name) VALUES ('trace trap');
INSERT INTO insn_minor_type (name) VALUES ('invop trap');
INSERT INTO insn_minor_type (name) VALUES ('oflow trap');
INSERT INTO insn_minor_type (name) VALUES ('halt');
INSERT INTO insn_minor_type (name) VALUES ('port in');
INSERT INTO insn_minor_type (name) VALUES ('port out');
INSERT INTO insn_minor_type (name) VALUES ('cpuid');
INSERT INTO insn_minor_type (name) VALUES ('sysctl');
INSERT INTO insn_minor_type (name) VALUES ('nop');
INSERT INTO insn_minor_type (name) VALUES ('unknown');

-- INSN_CPU:	The minimum CPU model supporting an instruction
CREATE TABLE insn_cpu (
	id		serial	PRIMARY KEY,
	name		varchar(32)
);

INSERT INTO insn_cpu (name) VALUES ('Unknown');

-- INSN_ISA:	The CPU Instruction Set, or Subset, containing an insn
CREATE TABLE insn_isa (
	id		serial	PRIMARY KEY,
	name		varchar(32)
);

INSERT INTO insn_isa (name) VALUES ('Unknown');
INSERT INTO insn_isa (name) VALUES ('General Purpose');
INSERT INTO insn_isa (name) VALUES ('Floating Point');
INSERT INTO insn_isa (name) VALUES ('System');


-- INSN_DEF: 	Definition of a CPU instruction. These are shared among 
-- 		INSTRUCTION table entries. They can be considered
--		instruction types. All invariant info about an instruction
--              is stored here: mnemonic, operand, bytes, etc. The larger
--              an asm file is, the more redundancy there is likely to
--              be amongst instructions, so this should end up saving a
--              lot of space -- no need to store every xor eax, eax .
CREATE TABLE insn_def (
	id		serial	PRIMARY KEY,
	major_type	integer REFERENCES insn_major_type(id)	DEFAULT 1,
	minor_type	integer REFERENCES insn_minor_type(id)	DEFAULT 1,
	mnemonic	varchar(16),	-- duh
	flags_set	varchar(128),	-- flags that are modified, ORed
	flags_tested	varchar(128),	-- flags that are tested, ORed
	prefixes	varchar(128),	-- all prefixes ORed together
	prefix_mnemonic	varchar(128),	-- prefixes with mnemonics
	bytes		bytea,		-- bytes in instruction
	signature	bytea,
	size		integer,
	stack_mod	integer,	-- stack modification
	-- make these string tables
	cpu		varchar(16),
	isa		varchar(16),
	-- BGO Class and Disassembler Module name
	class		integer REFERENCES module_class(id),
	-- descriptive info not yet provided by libdisasm
	title		varchar(64),
	description	varchar(256),
	pseudocode	bytea		DEFAULT NULL
);

-- index on mnemonic and prefixes required for testing existence of insn_def
CREATE INDEX insn_def_mnemonic_idx ON insn_def(mnemonic);
CREATE INDEX insn_def_prefixes_idx ON insn_def(prefixes);
-- applications are likely to query based on major or minor type
--CREATE INDEX insn_def_major_idx ON insn_def(major_type);
--CREATE INDEX insn_def_minor_idx ON insn_def(minor_type);
-- users are likely to query on CPU or ISA type
--CREATE INDEX insn_def_cpu_idx ON insn_def(cpu);
--CREATE INDEX insn_def_isa_idx ON insn_def(isa);

-- INSTRUCTION:	An instance of an INSN_DEF. A completeley disassembled
--		instruction. This table contains all insn info that
--              will vary with each disassembled instruction.
CREATE TABLE instruction (
	id		serial	PRIMARY KEY,
	file_offset	bigint,	-- offset (from file start)
	address		bigint,	-- load address
	insn_def	integer REFERENCES insn_def(id)
);

-- there will be a lot of lookups up file_offset and address
--CREATE INDEX instruction_offset_idx ON instruction(file_offset);
CREATE INDEX instruction_address_idx ON instruction(address);
-- applications are likely to query on insn definition
--CREATE INDEX instruction_def_idx ON instruction(insn_def);

CREATE VIEW bgo_insn AS 
	SELECT i.id, i.file_offset, i.address, id.major_type, id.minor_type,
	       id.mnemonic, id.flags_set, id.flags_tested, id.prefixes,
	       id.prefix_mnemonic, id.bytes, id.stack_mod, id.cpu, id.isa,
	       id.title, id.description, id.pseudocode
	FROM instruction i, insn_def id
	WHERE i.insn_def = id.id;

-- LAYER_INSN_MAP : All instructions contained in a code layer. In the case
-- of self-modifying code, a new layer will be created and the 
-- new disassembled code will be added to the new layer. Program overlays
-- can be handled with this as well.
-- NOTE: that there is no file_insn_map table. Instructions are mapped onto
--       layer 0 by default.
CREATE TABLE layer_insn_map (
	id		serial	PRIMARY KEY,
	layer		integer REFERENCES layer(id),
	insn		integer REFERENCES instruction(id)
);

CREATE INDEX layer_insn_map_layer_idx ON layer_insn_map(layer);
CREATE INDEX layer_insn_map_insn_idx ON layer_insn_map(insn);

-- SECTION_INSN_MAP : all instructions contained in a section
CREATE TABLE section_insn_map (
	id		serial	PRIMARY KEY,
	section		integer REFERENCES section(id),
	insn		integer REFERENCES instruction(id)
);

CREATE INDEX section_insn_map_section_idx ON section_insn_map(section);
CREATE INDEX section_insn_map_insn_idx ON section_insn_map(insn);

-- OP_REG : Register operand.
CREATE TABLE op_reg (
	id		serial	PRIMARY KEY,
	reg_id		integer,
	mnemonic	varchar(12),
	type		varchar(64),
	size		integer,
	alias		integer REFERENCES op_reg(id)	DEFAULT NULL,
	alias_shift	integer
);

--CREATE INDEX op_reg_regid_idx ON op_reg(reg_id);
--CREATE INDEX op_reg_mnemonic_idx ON op_reg(mnemonic);
--CREATE INDEX op_reg_alias_idx ON op_reg(alias);

-- OP_BIT : Flag (bit) operand.
CREATE TABLE op_bit (
	id		serial	PRIMARY KEY,
	mnemonic	varchar(8),
	name		varchar(20),
	-- register containing this flag
	reg		integer REFERENCES op_reg(id)	DEFAULT NULL,
	-- position in register
	position	integer
);

--CREATE INDEX op_bit_mnemonic_idx ON op_bit(mnemonic);
--CREATE INDEX op_bit_position_idx ON op_bit(position);

-- OP_IMM : Immediate operand.
CREATE TABLE op_imm (
	id		serial	PRIMARY KEY,
	value		bigint
);

--CREATE INDEX op_imm_value_idx ON op_imm(value);

-- OP_REL : Relative (to %pc) operand.
CREATE TABLE op_rel (
	id		serial	PRIMARY KEY,
	value		bigint,
	file_offset	bigint,
	address		bigint
);

--CREATE INDEX op_rel_value_idx ON op_rel(value);
--CREATE INDEX op_rel_addr_idx ON op_rel(address);

-- OP_EXPR : Effective Address operand.
CREATE TABLE op_expr (
	id		serial	PRIMARY KEY,
	base		integer references op_reg(id)	DEFAULT NULL,	-- base 
	idx		integer references op_reg(id)	DEFAULT NULL,	-- index
	scale		integer,
	disp		bigint				-- displacement
);

--CREATE INDEX op_expr_base_idx ON op_expr(base);
--CREATE INDEX op_expr_disp_idx ON op_expr(disp);

-- OP_TYPE : Operand type.
CREATE TABLE op_type (
	id		integer PRIMARY KEY,
	name		varchar(16),
	table_name	varchar(16)
);

INSERT INTO op_type (id, name, table_name) VALUES (1, 'Unknown', 'op_imm');
INSERT INTO op_type (id, name, table_name) VALUES (2, 'Register', 'op_reg');
INSERT INTO op_type (id, name, table_name) VALUES (3, 'Immediate', 'op_imm');
INSERT INTO op_type (id, name, table_name) VALUES (4, 'RelativeNear', 'op_rel');
INSERT INTO op_type (id, name, table_name) VALUES (5, 'RelativeFar', 'op_rel');
INSERT INTO op_type (id, name, table_name) VALUES (6, 'Absolute', 'op_imm');
INSERT INTO op_type (id, name, table_name) VALUES (7, 'Offset', 'op_imm');
INSERT INTO op_type (id, name, table_name) VALUES (8, 'Bit', 'op_bit');
INSERT INTO op_type (id, name, table_name) VALUES (9, 'EffectiveAddress', 
       'op_exp');

-- OP_DEF:	Operand definition. Like INSN_DEF, these are 'types' of
--		operands which are referenced by the OPERAND table entries.
--              Many-to-many. Operand definitions are reused by all insns.
CREATE TABLE op_def (
	id		serial	PRIMARY KEY,
	type		integer REFERENCES op_type(id),	-- Operand type
	-- value is the id of the operand in the appropriate table (cf type)
	value		integer	 
);

--CREATE INDEX op_def_type_idx ON op_def(type);
CREATE INDEX op_def_value_idx ON op_def(value);

CREATE VIEW operand_register AS
	SELECT d.id, r.reg_id, r.mnemonic, r.type, r.size, 
		a.reg_id as alias_id, a.mnemonic as alias_mnemonic, 
		r.alias_shift
	FROM op_def d, op_reg r
	LEFT JOIN op_reg a ON a.id = r.alias
	WHERE d.type = 2 AND d.value = r.id;

CREATE VIEW operand_immediate AS
	SELECT d.id, i.value FROM op_def d, op_imm i
	WHERE d.type = 3 AND d.value = i.id;

CREATE VIEW operand_relative_far AS
	SELECT d.id, i.value FROM op_def d, op_imm i
	WHERE d.type = 4 AND d.value = i.id;

CREATE VIEW operand_relative_near AS
	SELECT d.id, i.value FROM op_def d, op_imm i
	WHERE d.type = 5 AND d.value = i.id;

CREATE VIEW operand_absolute AS
	SELECT d.id, i.value FROM op_def d, op_imm i
	WHERE d.type = 6 AND d.value = i.id;

CREATE VIEW operand_offset AS
	SELECT d.id, i.value FROM op_def d, op_imm i
	WHERE d.type = 7 AND d.value = i.id;

CREATE VIEW operand_effective_addr AS
	SELECT d.id, b.mnemonic AS base, i.mnemonic AS idx, e.scale, e.disp 
	FROM op_def d, op_expr e LEFT JOIN op_reg b ON b.id = e.base 
	LEFT JOIN op_reg i ON i.id = e.idx 
	WHERE d.type = 8 AND d.value = e.id;

CREATE TABLE op_datatype (
	id		integer PRIMARY KEY,
	name		varchar(24)
);

INSERT INTO op_datatype (name, id) VALUES ('unknown', 1);
INSERT INTO op_datatype (name, id) VALUES ('byte', 2);
INSERT INTO op_datatype (name, id) VALUES ('hword', 3);
INSERT INTO op_datatype (name, id) VALUES ('word', 4);
INSERT INTO op_datatype (name, id) VALUES ('dword', 5);
INSERT INTO op_datatype (name, id) VALUES ('qword', 6);
INSERT INTO op_datatype (name, id) VALUES ('dqword', 7);
INSERT INTO op_datatype (name, id) VALUES ('single real', 8);
INSERT INTO op_datatype (name, id) VALUES ('double real', 9);
INSERT INTO op_datatype (name, id) VALUES ('extended real', 10);
INSERT INTO op_datatype (name, id) VALUES ('binary coded decimal', 11);
INSERT INTO op_datatype (name, id) VALUES ('packed single simd', 12);
INSERT INTO op_datatype (name, id) VALUES ('packed double simd', 13);
INSERT INTO op_datatype (name, id) VALUES ('scalar single simd', 14);
INSERT INTO op_datatype (name, id) VALUES ('scalar double simd', 15);
INSERT INTO op_datatype (name, id) VALUES ('descriptor 16', 16);
INSERT INTO op_datatype (name, id) VALUES ('descriptor 32', 17);
INSERT INTO op_datatype (name, id) VALUES ('pseudo descriptor 16', 18);
INSERT INTO op_datatype (name, id) VALUES ('pseudo descriptor 32', 19);
INSERT INTO op_datatype (name, id) VALUES ('fpu environment', 20);
INSERT INTO op_datatype (name, id) VALUES ('fpu simd register state', 21);

-- INSN_OP_DEF_MAP : Map operands to an instruction definition.
CREATE TABLE insn_op_def_map (
	id		serial	PRIMARY KEY,
	insn_def	integer REFERENCES insn_def(id),
	op_def		integer REFERENCES op_def(id),
	name		varchar(8),	-- name of operand (dest, src1, src2)
	datatype	integer REFERENCES op_datatype(id)	DEFAULT 1,
	flags		varchar(128),
	size		integer,	-- Size of operand in bytes
	ord		integer,	-- Order (0, 1, 2, 3...)
	access		integer		-- RWX
);

--CREATE INDEX insn_op_def_map_insn_idx ON insn_op_def_map(insn_def);
--CREATE INDEX insn_op_def_map_op_idx ON insn_op_def_map(op_def);
--CREATE INDEX insn_op_def_map_ord_idx ON insn_op_def_map(ord);
--CREATE INDEX insn_op_def_map_name_idx ON insn_op_def_map(name);
--CREATE INDEX insn_op_def_map_access_idx ON insn_op_def_map(access);
--CREATE INDEX insn_op_def_map_flag_idx ON insn_op_def_map(flags);

CREATE VIEW instruction_operand AS
	SELECT m.insn_def, m.ord AS op_order, m.name, t.name AS type, 
		dt.name AS datatype, m.access, m.flags, m.size, 
		r.mnemonic AS register, r.type AS register_type, 
		r.size AS register_size, 
		a.mnemonic AS register_alias, a.type AS register_alias_type, 
		r.alias_shift AS register_alias_shift,
		i.value AS immediate,
		eb.mnemonic AS eaddr_base, eb.type AS eaddr_base_type, 
		eba.mnemonic AS eaddr_base_alias,
		ei.mnemonic AS eaddr_index, ei.type AS eaddr_index_type,
		eia.mnemonic AS eaddr_index_alias,
		e.scale AS eaddr_scale, e.disp AS eaddr_disp
	FROM insn_op_def_map m 
		JOIN op_def d ON m.op_def = d.id
		JOIN op_type t ON d.type = t.id
		JOIN op_datatype dt ON m.datatype = dt.id
		LEFT JOIN op_reg r ON r.id = d.value AND d.type = 2 
		LEFT JOIN op_reg a ON a.id = r.alias
		LEFT JOIN op_imm i ON i.id = d.value AND d.type in (3,4,5,6,7)
		LEFT JOIN op_expr e ON e.id = d.value AND d.type = 8
		LEFT JOIN op_reg eb ON e.base = eb.id
		LEFT JOIN op_reg eba ON eb.alias = eba.id
		LEFT JOIN op_reg ei ON e.idx = ei.id
		LEFT JOIN op_reg eia ON ei.alias = eia.id
	ORDER BY m.insn_def, m.ord;
--	SELECT m.insn_def, m.name AS name, t.name AS type, dt.name AS datatype,
--		m.flags, m.size, m.ord, m.access, d.value AS op_id 
--	FROM insn_op_def_map m, op_type t, op_datatype dt, op_def d 
--	WHERE m.op_def = d.id AND d.type = t.id AND m.datatype = dt.id ;

	
-- OP_CONSTANT_TYPE : Determines which part of the operand the constant
--                    refers to. Only needed for Effective Address operands.
CREATE TABLE op_constant_type (
	id		integer PRIMARY KEY,
	name		varchar(16)
);

INSERT INTO op_constant_type (id, name) VALUES (1, 'Register');
INSERT INTO op_constant_type (id, name) VALUES (2, 'Immediate');
INSERT INTO op_constant_type (id, name) VALUES (3, 'EAddr Disp');
INSERT INTO op_constant_type (id, name) VALUES (4, 'EAddr Base');
INSERT INTO op_constant_type (id, name) VALUES (5, 'EAddr Index');


-- =========================================================================
--                  Insn Containers: Functions, blocks
-- =========================================================================


-- BLOCK : A language-level block of code, e.g. stuff between curly braces
--         in C. Useful for scoping and for denoting language-level control
--         flow structures.
create table block (
	id		serial	PRIMARY KEY,
	container	integer references block(id),
	-- support for control flow constructs: instructions that begin
	-- the block loop init, loop/execution condition, and loop terminus
	block_init	integer REFERENCES instruction(id)	DEFAULT NULL,
	block_cond	integer REFERENCES instruction(id)	DEFAULT NULL,
	block_term	integer REFERENCES instruction(id)	DEFAULT NULL
);

-- BLOCK_ENTRY_MAP: all instructions where execution enters a code block
CREATE TABLE block_entry_map (
	id		serial	PRIMARY KEY,
	block		integer REFERENCES block(id),
	insn		integer REFERENCES instruction(id)
);

CREATE INDEX block_entry_map_block_idx ON block_entry_map(block);
CREATE INDEX block_entry_map_insn_idx ON block_entry_map(insn);

-- BLOCK_EXIT_MAP: all instructions where execution leaves a code block
CREATE TABLE block_exit_map (
	id		serial	PRIMARY KEY,
	block		integer REFERENCES block(id),
	insn		integer REFERENCES instruction(id)
);

CREATE INDEX block_exit_map_block_idx ON block_exit_map(block);
CREATE INDEX block_exit_map_insn_idx ON block_exit_map(insn);

-- BLOCK_INSN_MAP: all instructions contained in a code block
CREATE TABLE block_insn_map (
	id		serial	PRIMARY KEY,
	block		integer REFERENCES block(id),
	insn		integer REFERENCES instruction(id)
);

CREATE INDEX block_insn_map_block_idx ON block_insn_map(block);
CREATE INDEX block_insn_map_insn_idx ON block_insn_map(insn);

-- FN_CALL_CONVENTION : Function calling conventions
CREATE TABLE fn_call_convention (
	id		integer PRIMARY KEY,
	name		varchar(16),
	c_stack_ord	boolean,	-- args pushed c or pascal style?
	caller_cleanup	boolean
);

INSERT INTO fn_call_convention (id, name, c_stack_ord, caller_cleanup)
VALUES (1, 'cdecl', 'true', 'true');
INSERT INTO fn_call_convention (id, name, c_stack_ord, caller_cleanup)
VALUES (2, 'stdcall', 'true', 'false');
INSERT INTO fn_call_convention (id, name, c_stack_ord, caller_cleanup)
VALUES (3, 'pascal', 'false', 'false');
INSERT INTO fn_call_convention (id, name, c_stack_ord, caller_cleanup)
VALUES (4, 'fastcall', 'false', 'false');


-- FUNCTION : A language-level function, optionally with arguments and
--            a return value
CREATE TABLE function (
	id		serial	PRIMARY KEY,
	name		varchar(256),
	entry		integer REFERENCES block(id),
	ret_type	integer REFERENCES datatype(id)		DEFAULT NULL,
	convention	integer REFERENCES fn_call_convention(id) DEFAULT 1
);

CREATE INDEX function_name_idx ON function(name);
CREATE INDEX function_entry_idx ON function(entry);

-- FUNCTION_ARG : An argument or parameter to a function. Can be associated
--                with more than one function to save space, e.g. 'FILE *'
CREATE TABLE function_arg (
	id		serial	PRIMARY KEY,
	name		varchar(256),
	datatype	integer REFERENCES datatype(id)
);

CREATE INDEX function_arg_name_idx ON function_arg(name);

-- FN_ARG_MAP : Arguments or params to a function
CREATE TABLE fn_arg_map (
	id		serial	PRIMARY KEY,
	func		integer references function(id),
	arg		integer references function_arg(id),
	ord		integer	-- order of argument: 0, 1, 2 etc
);

CREATE INDEX fn_arg_map_func_idx ON fn_arg_map(func);
CREATE INDEX fn_arg_map_arg_idx ON fn_arg_map(arg);
CREATE INDEX fn_arg_map_ord_idx ON fn_arg_map(ord);

-- FN_EXIT_MAP : All instructions where execution leaves a function 
CREATE TABLE fn_exit_map (
	id		serial	PRIMARY KEY,
	fn		integer REFERENCES function(id),
	insn		integer REFERENCES instruction(id)
);

CREATE INDEX fn_exit_map_fn_idx ON fn_exit_map(fn);
CREATE INDEX fn_exit_map_insn_idx ON fn_exit_map(insn);

-- FN_INSN_MAP : All instructions in a function
CREATE TABLE fn_insn_map (
	id		serial	PRIMARY KEY,
	fn		integer REFERENCES function(id),
	insn		integer REFERENCES instruction(id)
);

CREATE INDEX fn_insn_map_fn_idx ON fn_insn_map(fn);
CREATE INDEX fn_insn_map_insn_idx ON fn_insn_map(insn);

-- MACRO: A symbolic grouping of instructions for folding purposes. A
--        C-style code macro.
CREATE TABLE macro (
	id		serial	PRIMARY KEY,
	name		varchar(256)
);

CREATE INDEX macro_name_idx ON macro(name);

-- MACRO_INSN_MAP: A contiguous group of instructions in a macro
CREATE TABLE macro_insn_map (
	id		serial	PRIMARY KEY,
	macro		integer REFERENCES macro(id),
	insn		integer REFERENCES instruction(id)
);

CREATE INDEX macro_insn_map_macro_idx ON macro_insn_map(macro);
CREATE INDEX macro_insn_map_insn_idx ON macro_insn_map(insn);

-- =========================================================================
--                           (Cross) References 
-- =========================================================================

-- CODEREF
create table code_ref (
	id		serial	PRIMARY KEY,
	from_addr	integer REFERENCES instruction(id),
	to_addr		integer REFERENCES instruction(id),
	access		integer
);

CREATE INDEX code_ref_from_idx ON code_ref(from_addr);
CREATE INDEX code_ref_to_idx ON code_ref(to_addr);
--CREATE INDEX code_ref_access_idx ON code_ref(access);

-- DATAREF
create table data_ref (
	id		serial	PRIMARY KEY,
	from_addr	integer REFERENCES instruction(id),
	to_addr		integer REFERENCES data(id),
	access		integer
);

CREATE INDEX data_ref_from_idx ON data_ref(from_addr);
CREATE INDEX data_ref_to_idx ON data_ref(to_addr);

-- FUNCREF
create table func_ref (
	id		serial	PRIMARY KEY,
	from_addr	integer REFERENCES instruction(id),
	to_addr		integer REFERENCES function(id),
	access		integer
);

CREATE INDEX func_ref_from_idx ON func_ref(from_addr);
CREATE INDEX func_ref_to_idx ON func_ref(to_addr);

-- FILEREF
create table file_ref (
	id		serial	PRIMARY KEY,
	from_addr	integer REFERENCES instruction(id),
	to_addr		integer REFERENCES file(id),
	access		integer
);

CREATE INDEX file_ref_from_idx ON file_ref(from_addr);
CREATE INDEX file_ref_to_idx ON file_ref(to_addr);

-- =========================================================================
--           User-defined symbols, comments, and constats
-- =========================================================================

-- SCOPE:	scope of a symbol
create table scope (
	id		integer PRIMARY KEY,
	name		varchar(32)
);

-- global to project
INSERT INTO scope (id, name) VALUES (1, 'global');
-- local to file
INSERT INTO scope (id, name) VALUES (2, 'file');
-- local to section
INSERT INTO scope (id, name) VALUES (3, 'section');
-- local to function (e.g. parameters)
INSERT INTO scope (id, name) VALUES (4, 'function');
-- local to codeblock
INSERT INTO scope (id, name) VALUES (5, 'block');

-- SYM_TYPE:
CREATE TABLE symbol_type (
	id		integer PRIMARY KEY,
	name		varchar(64)
);

-- code label includes function names
INSERT INTO symbol_type (id, name) VALUES ( 1, 'code label' );
INSERT INTO symbol_type (id, name) VALUES ( 2, 'string' );
INSERT INTO symbol_type (id, name) VALUES ( 3, 'variable' );
INSERT INTO symbol_type (id, name) VALUES ( 4, 'import' );
INSERT INTO symbol_type (id, name) VALUES ( 5, 'source code line' );

-- SYMBOL:
CREATE TABLE symbol (
	id		serial	PRIMARY KEY,
	name		varchar(256),
	file_offset	bigint,
	load_addr	bigint,
	type		integer REFERENCES symbol_type(id),
	--  scope defaults to 'file'
	scope		integer REFERENCES scope(id)	DEFAULT 2
);

CREATE INDEX symbol_name_idx ON symbol(name);
CREATE INDEX symbol_offset_idx ON symbol(file_offset);
CREATE INDEX symbol_address_idx ON symbol(load_addr);

-- PROJECT_SYMBOL_MAP : All symbols associated with a project
CREATE TABLE project_symbol_map (
	id		serial	PRIMARY KEY,
	project		integer REFERENCES project(id),
	symbol		integer REFERENCES symbol(id)
);

CREATE INDEX project_symbol_map_proj_idx ON project_symbol_map(project);
CREATE INDEX project_symbol_map_sym_idx ON project_symbol_map(symbol);

-- FILE_SYMBOL_MAP : All symbols associated with a file
CREATE TABLE file_symbol_map (
	id		serial	PRIMARY KEY,
	file		integer REFERENCES file(id),
	symbol		integer REFERENCES symbol(id)
);

CREATE INDEX file_symbol_map_file_idx ON file_symbol_map(file);
CREATE INDEX file_symbol_map_sym_idx ON file_symbol_map(symbol);

-- SECTION_SYMBOL_MAP : All symbols associated with a section
CREATE TABLE section_symbol_map (
	id		serial	PRIMARY KEY,
	section		integer REFERENCES section(id),
	symbol		integer REFERENCES symbol(id)
);

CREATE INDEX section_symbol_map_sec_idx ON section_symbol_map(section);
CREATE INDEX section_symbol_map_sym_idx ON section_symbol_map(symbol);

-- FUNCTION_SYMBOL_MAP : All symbols associated with a function
CREATE TABLE function_symbol_map (
	id		serial	PRIMARY KEY,
	function	integer REFERENCES function(id),
	symbol		integer REFERENCES symbol(id)
);

CREATE INDEX function_symbol_map_func_idx ON function_symbol_map(function);
CREATE INDEX function_symbol_map_sym_idx ON function_symbol_map(symbol);

-- BLOCK_SYMBOL_MAP : All symbols associated with a block
CREATE TABLE block_symbol_map (
	id		serial	PRIMARY KEY,
	block		integer REFERENCES block(id),
	symbol		integer REFERENCES symbol(id)
);

CREATE INDEX block_symbol_map_block_idx ON block_symbol_map(block);
CREATE INDEX block_symbol_map_sym_idx ON block_symbol_map(symbol);

-- CONSTANT: A symbolic constant, such as a C enumeration or #define
CREATE TABLE constant (
	id		serial	PRIMARY KEY,
	name		varchar(256),
	value		bigint,
	-- lame hack to support float constants as well
	is_float	bool	DEFAULT 'False',
	f_value		float
);

CREATE INDEX constant_name_idx ON constant(name);
CREATE INDEX constant_value_idx ON constant(value);
CREATE INDEX constant_f_value_idx ON constant(f_value);

-- CONSTANT_NAMESPACE : a collection of related constants, e.g. the
--                      group of enumerstions in a C enum {} statement.
CREATE TABLE constant_namespace (
	id		serial	PRIMARY KEY,
	name		varchar(256),
	--  scope defaults to 'global'
	scope		integer REFERENCES scope(id)	DEFAULT 1
);

CREATE INDEX constant_namespace_name_idx ON constant_namespace(name);

-- CONSTANT_NAMESPACE_MAP : Associates constants with a constant namespace
CREATE TABLE constant_namespace_map (
	id		serial	PRIMARY KEY,
	constant	integer REFERENCES constant(id),
	namespace	integer REFERENCES constant_namespace(id)
);

CREATE INDEX const_namespace_map_const_idx ON constant_namespace_map(constant);
CREATE INDEX const_namespace_map_name_idx ON constant_namespace_map(namespace);

-- INSN_CONSTANT_MAP : Map constants onto operands in an instruction. There
--                     should be only 1 constant for each operand, except for
--                     effective address operands which can have 3 (one for
--                     base, index, and disp). The 'op' field refers to the
--                     'ord' column for the operand in its insn_op_def_map.
CREATE TABLE insn_constant_map (
	id		serial	PRIMARY KEY,
	insn		integer references instruction(id),
	-- 'op' is the order # of the operand in the insn
	op		integer,
	type		integer references op_constant_type(id),
	constant	integer references constant(id)
);

CREATE INDEX insn_constant_map_insn_idx ON insn_constant_map(insn);
CREATE INDEX insn_constant_map_op_idx ON insn_constant_map(op);
CREATE INDEX insn_constant_map_const_idx ON insn_constant_map(constant);

-- DATA_CONSTANT_MAP : Map constants onto data addresses
CREATE TABLE data_constant_map (
	id		serial	PRIMARY KEY,
	data		integer references data(id),
	constant	integer references constant(id)
);

CREATE INDEX data_constant_map_data_idx ON data_constant_map(data);
CREATE INDEX data_constant_map_const_idx ON data_constant_map(constant);

-- COMMENT:	Arbitrary text attached to a project, file, section,
--		instruction, etc.
CREATE TABLE user_comment (
	id		serial	PRIMARY KEY,		-- ID from sequence
	repeat		boolean,	-- Make repeatable? (IDA users :P)
	text		varchar(512),
	-- timestamp allows comments to be used as a log as well
	timestamp	timestamp	DEFAULT now()
);

-- Comment a Project object
CREATE TABLE project_comment_map (
	id		serial	PRIMARY KEY,
	project		integer REFERENCES project(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX project_comment_proj_map_idx ON project_comment_map(project);

-- Comment a Layer object
CREATE TABLE layer_comment_map (
	id		serial	PRIMARY KEY,
	layer		integer REFERENCES layer(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX layer_comment_map_layer_idx ON layer_comment_map(layer);

-- Comment a File object
CREATE TABLE file_comment_map (
	id		serial	PRIMARY KEY,
	file		integer REFERENCES file(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX file_comment_map_file_idx ON file_comment_map(file);

-- Comment a Section object
CREATE TABLE section_comment_map (
	id		serial	PRIMARY KEY,
	section		integer REFERENCES section(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX section_comment_sec_map_idx ON section_comment_map(section);

-- Comment a Function object
CREATE TABLE function_comment_map (
	id		serial	PRIMARY KEY,
	function	integer REFERENCES function(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX function_comment_func_map_idx ON function_comment_map(function);

-- Comment a Block object
CREATE TABLE block_comment_map (
	id		serial	PRIMARY KEY,
	block		integer REFERENCES block(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX block_comment_map_block_idx ON block_comment_map(block);

-- Comment an Instruction object
CREATE TABLE insn_comment_map (
	id		serial	PRIMARY KEY,
	insn		integer REFERENCES instruction(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX insn_comment_map_insn_idx ON insn_comment_map(insn);


-- Comment am Insn_Def object ('repeatable' comment)
CREATE TABLE insn_def_comment_map (
	id		serial	PRIMARY KEY,
	insn_def	integer REFERENCES insn_def(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX insn_def_comment_def_map ON insn_def_comment_map(insn_def);

-- Comment an Operand_Def object
CREATE TABLE op_def_comment_map (
	id		serial	PRIMARY KEY,
	op_def		integer REFERENCES op_def(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX op_def_comment_def_map ON op_def_comment_map(op_def);

-- Comment a Constant object
CREATE TABLE constant_comment_map (
	id		serial	PRIMARY KEY,
	constant	integer REFERENCES constant(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX constant_comment_const_map_idx ON constant_comment_map(constant);

-- Comment a Data object
CREATE TABLE data_comment_map (
	id		serial	PRIMARY KEY,
	data		integer REFERENCES data(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX data_comment_map_data_idx ON data_comment_map(data);

-- Comment a Symbol object
CREATE TABLE symbol_comment_map (
	id		serial	PRIMARY KEY,
	symbol		integer REFERENCES symbol(id),
	comment		integer REFERENCES user_comment(id)
);

CREATE INDEX symbol_comment_sym_map_idx ON symbol_comment_map(symbol);
	"""

# Copyright (c) 2012 Yuri K. Schlesner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import renpy.ast as ast

def pretty_print_ast(out_file, ast):
    for stmt in ast:
        print_statement(out_file, stmt, 0)

def indent(f, level):
    # Print indentation
    f.write(u'    ' * level)

def print_statement(f, statement, indent_level=0):
    indent(f, indent_level)

    func = statement_printer_dict.get(statement.__class__, print_Unknown)
    func(f, statement, indent_level)

def escape_string(s):
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\t', '\\t')
    return s

def print_atl(f, atl_block, indent_level):
    indent(f, indent_level)

    # TODO print ATL
    f.write(u"TODO atl\n")

def print_imspec(f, imspec):
    if imspec[1] is not None: # Expression
        # TODO expression
        f.write(u"TODO expression")
    else: # Image name
        f.write(' '.join(imspec[0]))

    # at
    if len(imspec[3]) > 0:
        # TODO at_list
        f.write(u" at TODO")

    # as
    if imspec[2] is not None:
        f.write(u" as %s" % (imspec[2], ))

    # behind
    if len(imspec[6]) > 0:
        # TODO behind
        f.write(u" behind TODO")

    # onlayer
    if imspec[4] != 'master':
        f.write(u" onlayer %s" % (imspec[4], ))

    # zorder
    # This isn't in the docs, but it's in the parser
    if imspec[5] is not None:
        f.write(u" zorder %s" % (imspec[5], ))

def print_Label(f, stmt, indent_level):
    f.write(u"label %s" % (stmt.name, ))
    if stmt.parameters is not None:
        # TODO parameters
        f.write(u"(parameters TODO)")
    f.write(u':\n')

    for sub_stmt in stmt.block:
        print_statement(f, sub_stmt, indent_level + 1)

def print_Say(f, stmt, indent_level):
    if stmt.who is not None:
        f.write(u"%s " % (stmt.who, ))
    f.write(u"\"%s\"" % (escape_string(stmt.what), ))
    if stmt.with_ is not None:
        f.write(u" with TODO")
        # TODO with_
    f.write(u'\n')

def print_Jump(f, stmt, indent_level):
    f.write(u"jump ")
    if stmt.expression:
        # TODO expression
        f.write(u"expression TODO")
    else:
        f.write(stmt.target)
    f.write(u'\n')

def print_Scene(f, stmt, indent_level):
    f.write(u"scene")
    if stmt.imspec is None:
        if stmt.layer != 'master':
            f.write(u" onlayer %s" % (stmt.layer, ))
    else:
        f.write(u' ')
        print_imspec(f, stmt.imspec)

    # with isn't handled here, but split in several statements

    if stmt.atl is not None:
        f.write(u':\n')
        print_atl(f, stmt.atl, indent_level+1)
    else:
        f.write('\n')

def print_With(f, stmt, indent_level):
    f.write(u"with %s\n" % (stmt.expr, ))

def print_Show(f, stmt, indent_level):
    f.write(u"show ")
    print_imspec(f, stmt.imspec)

    # with isn't handled here, but split in several statements

    if stmt.atl is not None:
        f.write(u':\n')
        print_atl(f, stmt.atl, indent_level+1)
    else:
        f.write('\n')

def print_Hide(f, stmt, indent_level):
    f.write(u"hide ")
    print_imspec(f, stmt.imspec)

    # with isn't handled here, but split in several statements

    f.write('\n')

def print_Python(f, stmt, indent_level):
    # TODO figure out what to do with 'early'
    code_src = stmt.code.source

    stripped_code = code_src.strip()

    if stripped_code.count('\n') == 0:
        f.write(u"$ %s\n" % (stripped_code, ))
    else:
        f.write(u"python")
        if stmt.hide:
            f.write(u" hide")
        f.write(u":\n")

        for line in code_src.splitlines(True):
            indent(f, indent_level + 1)
            f.write(line)

def print_Return(f, stmt, indent_level):
    f.write(u"return")

    if stmt.expression is not None:
        f.write(u" %s" % (stmt.expression, ))

    f.write(u'\n')

def print_UserStatement(f, stmt, indent_level):
    f.write(u"%s\n" % (stmt.line, ))

def print_Init(f, stmt, indent_level):
    # TODO what does stmt.priority do?
    f.write(u"init:\n")
    for s in stmt.block:
        print_statement(f, s, indent_level + 1)

def print_Image(f, stmt, indent_level):
    f.write(u"image %s" % (' '.join(stmt. imgname), ))
    if stmt.code is not None:
        f.write(u" = %s\n" % (stmt.code.source, ))
    else:
        f.write(u":\n")
        print_atl(f, stmt.atl, indent_level + 1)

def print_Transform(f, stmt, indent_level):
    f.write(u"transform %s" % (stmt.varname, ))

    paraminfo = stmt.parameters
    if paraminfo is not None:
        # not sure what the other fields of `paraminfo` do
        f.write(u"(")

        first = True
        for param in paraminfo.parameters:
            if first:
                first = False
            else:
                f.write(u", ")

            f.write(param[0])

            if param[1] is not None:
                f.write(u" = %s" % param[1])

        f.write(u")")

    f.write(":\n")
    print_atl(f, stmt.atl, indent_level + 1)

def print_Menu(f, stmt, indent_level):
    f.write(u"menu:\n")

    if stmt.with_ is not None:
        indent(f, indent_level + 1)
        f.write(u"with %s\n" % (stmt.with_, ))

    if stmt.set is not None:
        indent(f, indent_level + 1)
        f.write(u"set %s\n" % (stmt.with_, ))

    for item in stmt.items:
        indent(f, indent_level + 1)

        # caption
        f.write(u"\"%s\"" % (escape_string(item[0]), ))

        if item[2] is not None:
            # condition
            if item[1] != 'True':
                f.write(u" if %s" % (item[1], ))

            f.write(u':\n')

            for inner_stmt in item[2]:
                print_statement(f, inner_stmt, indent_level + 2)
        else:
            f.write(u'\n')

statement_printer_dict = {
        ast.Label: print_Label,
        ast.Say: print_Say,
        ast.Jump: print_Jump,
        ast.Scene: print_Scene,
        ast.With: print_With,
        ast.Show: print_Show,
        ast.Hide: print_Hide,
        ast.Python: print_Python,
        ast.Return: print_Return,
        ast.UserStatement: print_UserStatement,
        ast.Init: print_Init,
        ast.Image: print_Image,
        ast.Transform: print_Transform,
        ast.Menu: print_Menu,
    }

def print_Unknown(f, stmt, indent_level):
    print "Unknown AST node: %s" % (stmt.__class__.__name__, )
    f.write(u"<<<UNKNOWN NODE %s>>>\n" % (stmt.__class__.__name__, ))

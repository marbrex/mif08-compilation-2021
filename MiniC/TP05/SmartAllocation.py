from TP04.Operands import Offset, Temporary, S, Register, GP_REGS, FP
from TP04.Instruction3A import Instru3A
from TP04.SimpleAllocations import Allocator
from .LibGraphes import Graph  # For Graph coloring utility functions
from Errors import MiniCInternalError


def replace_smart(old_i):
    """Replace Temporary operands with the corresponding allocated
    physical register OR memory location."""
    before = []
    after = []
    ins, old_args = old_i.unfold()
    print("old_args:", old_args)
    args = []
    numreg = 1
    # TODO (lab5): compute before,after,args. This is similar to what
    # TODO (lab5): replace_mem and replace_reg from TP04 do.
    # and now return the new list!
    for arg in old_args:
        if isinstance(arg, Temporary):
            arg = arg.get_alloced_loc()
            if isinstance(arg, Offset):
                # need to check for is_read_only(), 'cause arguments
                # are not always of the form (source, destination)
                # both may be read-only
                if old_i.is_read_only():
                    before.append(Instru3A('ld', S[numreg], arg))
                else:
                    before.append(Instru3A('ld', S[numreg], arg)) # S : constant in Operands.py
                    after.append(Instru3A('sd', S[numreg], arg))
                args.append(S[numreg])
                numreg = numreg + 1
            elif isinstance(arg, Register):
                args.append(arg)
        else:
            args.append(arg)
    i = Instru3A(ins, args=args)  # change argument list into args
    return before + [i] + after


class SmartAllocator(Allocator):

    _igraph: Graph  # interference graph

    def __init__(self, function, basename, liveness,
                 debug=False, debug_graphs=False, *args):
        self._liveness = liveness
        self._basename = basename
        self._debug = debug
        self._debug_graphs = debug_graphs
        super().__init__(function, *args)

    def prepare(self):
        """Perform all steps related to smart register allocation:

        - Dataflow analysis to compute liveness range of each
          temporary.

        - Interference graph construction

        - Graph coloring

        - Substitution of temporaries by actual locations in the
          3-address code.
        """
        # prints the CFG as a dot file
        if self._debug_graphs:
            self._function_code.print_dot(self._basename + ".dot", view=True)
            print("CFG generated in " + self._basename + ".dot.pdf")

        # liveness analysis
        # set the following sets for each block:
        # GEN and KILL (CFG.set_gen_kill()),
        # IN and OUT (LivenessDataFlow.run_dataflow_analysis())
        self._liveness.run()

        # conflict graph
        self.build_interference_graph()

        if self._debug_graphs:
            print("printing the conflict graph")
            self._igraph.print_dot(self._basename + "_conflicts.dot")

        # Smart Alloc via graph coloring
        self.smart_alloc(self._basename + "_colored.dot")

    def rewriteCode(self, listcode):
        # Finally, modify the code to replace temporaries with
        # regs/memory locations
        self._function_code.iter_instructions(replace_smart)

    def interfere(self, t1, t2):
        """Interfere function: True if t1 and t2 are in conflit anywhere in
        the function."""
        for instr, liveout in self._liveness._liveout.items():
            if set([t1,t2]).issubset(liveout):
                return True
            elif t1 in liveout and t2 in instr.defined():
                return True
            elif t2 in liveout and t1 in instr.defined():
                return True
        return False
        # raise NotImplementedError("interfere() function (lab5)") # TODO

    def build_interference_graph(self):
        """Build the interference graph. Nodes of the graph are temporaries,
        and an edge exists between temporaries iff they are in conflict (i.e.
        iff self.interfere(t1, t2)."""
        self._igraph = Graph()
        t = self._function_code._pool._all_temps
        for v in t:
            # print("add vertex "+str(v))
            self._igraph.add_vertex(v)
        tpairs = [(p1, p2) for p1 in t for p2 in t]
        # print(tpairs)
        for (t1, t2) in tpairs:
            if t1 == t2:
                continue  # A temporary cannot conflict with itself
            if self.interfere(t1, t2):
                # print("add edge "+str(t1)+" - "+str(t2))
                self._igraph.add_edge((t1, t2))

    def smart_alloc(self, outputname):
        """Allocate all temporaries with graph coloring
        also prints the colored graph if debug.

        Precondition: the interference graph (_igraph) must have been
        initialized.
        """
        if not self._igraph:
            raise MiniCInternalError("hum, the interference graph seems to be empty")
            
        # Temporary -> Operand (register or offset) dictionary,
        # specifying where a given Temporary should be allocated:
        alloc_dict = {}

        # TODO (lab5): color the graph and get back the coloring (see
        # Graph.color() in LibGraphes.py). Then, construct a dictionary Temporary ->
        # Register or Offset. Our version is less than 15 lines
        # including debug log. You can get all temporaries in
        # self._function_code._pool._all_temps.

        coloring = self._igraph.color()
        nb_colors_needed = len(set(coloring.values()))
        regs = list(GP_REGS)
        nb_regs = len(GP_REGS)
        print("coloring:", coloring)
        print("nb_colors_needed:", nb_colors_needed)

        if self._debug_graphs:
            print("printing the colored conflict graph")
            self._igraph.print_dot(self._basename + "_conflicts_colored.dot", coloring)

        print("regs:", regs)
        print("nb_regs:", nb_regs)

        # a list that contains:
        # as index: color (or number of neighbours)
        # as value: list of temporaries
        temps_same_color = []
        for i in range(nb_colors_needed):
            temps_same_color.append([key for key, val in coloring.items() if val == i])
            if i < nb_regs:
                # on a assez de registres
                curr_reg = regs.pop(0) # on utilise et retire le premier registre
                for temp in temps_same_color[i]:
                    alloc_dict[temp] = curr_reg
            else:
                for temp in temps_same_color[i]:
                    alloc_dict[temp] = self._function_code.new_offset(FP)
                # on a plus de registres => offset

        print("temps_same_color:", temps_same_color)
        print("alloc_dict:", alloc_dict)
        print("regs after:", regs)

        # raise NotImplementedError("Allocation based on graph coloring (lab5)")
        self._function_code._pool.set_temp_allocation(alloc_dict)
        self._function_code._stacksize = self._function_code.get_offset()

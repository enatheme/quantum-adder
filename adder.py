from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import IBMQ, Aer, execute

def simple_adder(lhs, rhs): # string of bits
    print(lhs)
    print(rhs)
    assert(len(lhs) == len(rhs))
    len_arg = len(lhs)
    q = QuantumRegister(17) # we add 2 4 bits number, result will be in the last 5 bits (overflow)
    c = ClassicalRegister(5)
    qc = QuantumCircuit(q, c)
    assert(len(lhs) < 5)
    assert(len(rhs) < 5)

    for ii, yesno in enumerate(lhs):
        if yesno == '1':
            qc.x(ii)
    for ii, yesno in enumerate(rhs):
        if yesno == '1':
            qc.x(ii + 4)
    qc.barrier()
    for i in range(0, 4):
        # XOR Gate
        qc.cx(q[0 + i], q[8 + i])
        qc.cx(q[4 + i], q[8 + i])
        
        # apply carry over
        if i > 0:
            qc.cx(q[13 + i - 1], q[8 + i])
        
        # carry over (ND Gate)
        qc.ccx(q[0 + i], q[4 + i], q[13 + i])
        qc.ccx(q[0 + i], q[13 + i - 1], q[13 + i])
        qc.ccx(q[4 + i], q[13 + i - 1], q[13 + i])
        
    qc.barrier()
    qc.measure(q[8], c[0])
    qc.measure(q[9], c[1])
    qc.measure(q[10], c[2])
    qc.measure(q[11], c[3])
    return qc

def add_circuit(lhs, rhs):
    # int to string of bit
    l = bin(lhs)[2:][::-1]
    r = bin(rhs)[2:][::-1]
    
    len_diff = len(l) - len(r)
    if len_diff > 0: # lhs > rhs
        r += '0' * len_diff
    elif len_diff < 0: # rhs > lhs
        l += '0' * -len_diff
    result = simple_adder(l, r)
    return result

def add(lhs, rhs):
    qc = add_circuit(lhs, rhs)
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend = simulator, shots = 100).result()
    for each in result.get_counts().keys():
        return int(each, 2)

lhs = 1
rhs = 3

#qc = add_circuit(lhs, rhs)
#qc.draw(output='mpl')
#simulator = Aer.get_backend('qasm_simulator')
#result = execute(qc, backend = simulator, shots = 100).result()
#print(result.get_counts())
#from qiskit.tools.visualization import plot_histogram
#plot_histogram(result.get_counts(qc))

print(f"{lhs} + {rhs} = {add(lhs, rhs)}")

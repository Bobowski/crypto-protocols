import time

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair

trials = 100
group = PairingGroup("SS1024")
g = group.random(G1)
h = group.random(G1)
i = group.random(G2)


assert group.InitBenchmark(), "failed to initialize benchmark"
ts = time.time()
group.StartBenchmark(["CpuTime", "RealTime", "Mul", "Exp", "Pair", "Granular"])
for a in range(trials):
    j = g * h
    k = i ** group.random(ZR)
    t = (j ** group.random(ZR)) / h
    n = pair(h, i)
group.EndBenchmark()
print(time.time() - ts)

msmtDict = group.GetGeneralBenchmarks()
granDict = group.GetGranularBenchmarks()
print("<=== General Benchmarks ===>")
print("Results  := ", msmtDict)
print("<=== Granular Benchmarks ===>")
print("G1 mul   := ", granDict["Mul"][G1])
print("G2 exp   := ", granDict["Exp"][G2])

from typing import Callable

def index_transform(src: int, dest: int) -> Callable[[int], int]:
  """
  When moving an element from src to dest,
  the index of other elements would change in some way.
  Requires src != dest.
  """
  if src < dest:
    return lambda i: i - 1 if src < i <= dest else i
  else:
    return lambda i: i + 1 if dest <= i < src else i

def mix(arr: list[int], idxmap: dict[tuple[int, int], int]):
  for i, x in enumerate(arr):
    if x == 0: continue
    src = idxmap[i, x]
    dest = (src + x) % (len(arr) - 1)
    if x < 0 and dest == 0: dest = len(arr) - 1
    transform = index_transform(src, dest)
    for y in idxmap.keys(): idxmap[y] = transform(idxmap[y])
    idxmap[i, x] = dest

def decrypt(arr: list[int], repeat: int):
  idxmap = dict(((i, x), i) for i, x in enumerate(arr))
  for _ in range(repeat): mix(arr, idxmap)
  i0 = idxmap[arr.index(0), 0]
  target = {(i0 + i) % len(arr) for i in [1000, 2000, 3000]}
  return sum(
    x for (_, x), _ 
    in filter(lambda pair: pair[1] in target, idxmap.items())
  )

def solve(input: str):
  arr = [int(x) for x in input.strip().splitlines()]
  print(decrypt(arr, 1), decrypt([x * 811589153 for x in arr], 10))

solve("""
1
2
-3
3
-2
0
4
""")

solve("""
-3520
-4579
487
2027
7128
8512
-6655
7529
-1912
-9964
4814
-4353
-7276
-4132
-6640
8120
-4171
-1527
-9270
-1436
3155
7889
1390
5530
4122
7327
5625
-5640
6345
1770
8829
-7175
-6617
5556
2105
4329
4964
-1339
-9088
-5184
7763
4788
-1766
-5824
-8828
-6919
2828
286
9277
5032
-1447
-3677
1995
-9126
216
4697
-1346
-4064
-4812
8968
3067
7092
-9706
1693
-6413
418
-7124
-8405
-7454
-1139
9530
-4809
-5845
-8656
-5899
-3108
4757
-6595
-6752
-2532
6823
-220
-6707
3474
-7185
2253
9743
-8457
3946
1330
-253
-4898
-4823
2786
-2674
2955
-3498
4539
-9685
6688
8968
2435
-3545
5184
-4455
4223
-283
-7051
5100
8637
-4816
550
-3733
8758
2808
-5043
-6620
7971
8040
-2326
5291
3614
399
-5785
784
-1318
8061
3322
7221
-2779
-129
-2913
-6026
8974
-1315
2189
-7027
-1762
-2770
-3430
6047
6748
-9888
-2760
-9705
-5758
-2720
-5345
-8791
4312
-375
8517
-5207
-4754
7776
-5609
1108
4493
-646
-5377
8022
-8960
-5163
1915
-1776
-8413
-4110
815
-8509
9445
6712
-6323
-4851
-6379
2967
4701
60
-5520
555
-6197
-632
1939
-846
-8764
-8002
4216
-323
-979
-6152
-5901
7001
2125
921
-7274
-7277
-7798
2971
-2674
-7872
-7913
-8702
-60
5708
-1641
1870
-1918
-2272
4461
4526
8731
-1819
5840
9985
1354
-1035
3686
-2752
-5685
497
1421
-2982
-7293
5842
-4918
7751
2606
7791
5153
8683
4741
-394
1631
7713
-1961
4647
-1390
5609
-2578
-7116
-1129
1268
-7184
-9452
-8333
-2816
-4692
1026
-2202
-174
-7601
-7409
8035
-7012
-9898
-8916
-8360
-3026
-5997
-4861
5808
-4089
3598
8190
-9118
-3820
7859
-8281
4329
1120
-3337
-6528
-6988
-8396
4746
-4408
-7903
7507
-8192
7391
-7003
3353
-9484
-8648
-232
-1987
-6570
-672
7282
1897
-6839
-3033
-1856
-2286
4349
-3625
-1364
-8915
-3942
-3516
-4893
1550
8621
8707
-4312
-5831
3278
867
7791
-8118
6591
2576
-8358
8259
-1582
5558
-1183
-1595
-5132
380
-6197
1785
-2744
-7594
7121
5362
-1217
-8121
3965
7730
7228
8731
7804
-3040
-5938
-1873
1242
7575
-4390
9154
-9070
3230
2794
-190
-8927
-2983
8286
-3051
-377
-8284
-3839
7792
-9373
2335
6233
-2202
3639
4832
-1452
2247
2533
6604
1414
-9938
-8721
4653
1546
-101
3195
4547
5440
203
1208
8400
-3632
-3637
1557
-2274
-9729
-8982
-210
-1703
-5462
2175
-8192
4911
1457
-9371
6006
3288
3000
1280
-9735
8790
-3785
8017
6297
-8191
8102
-9898
2006
592
9113
-4676
2775
-9632
-6772
3026
9962
1373
7190
-4852
2108
-3858
4512
-6397
-4069
-2597
327
8817
-5809
-4568
5186
4135
-3524
4425
6435
3260
1019
1174
8557
9907
7925
-4458
3523
9661
3213
5175
-6508
-9267
-2184
4476
-1794
-8369
3561
-4865
4565
9965
-1865
-640
6164
3264
-9569
3220
-8700
-1234
-5263
3303
-948
6556
-6528
369
1393
6140
9346
307
-6971
5505
2376
2882
7070
-4978
-8561
8063
2253
490
-1790
6513
-4105
5008
677
481
-988
-7002
-2160
3913
-4120
2083
-3705
7803
-3419
8805
1893
-4852
-2116
-8914
-7255
2494
1863
340
-9007
-7162
6648
369
-5402
3641
-128
7256
-9988
-3019
9758
5804
-4620
2804
-871
-6433
-3749
-2519
-6664
7605
3264
-7932
1838
-2071
-607
2583
-7626
-3379
-1045
-8656
2686
6055
-6864
4653
4428
1980
5042
7836
-3465
1824
8383
1809
304
-7444
4135
5032
1508
-1
-4170
-8752
-874
-3216
5782
-975
-101
-1727
6071
4357
6462
-2033
4663
-5985
-1887
-8246
981
-5609
-6413
2772
6425
-6178
-1022
-74
-937
-8295
7742
437
3699
-8843
5494
9837
-791
5095
6556
-8898
880
-7319
5092
4415
-4538
-4577
8341
-471
7202
5368
-270
9859
-3604
6028
-513
8980
-7067
32
4768
-2632
9597
-2147
3753
2374
8290
-5650
2916
-7894
3546
4312
6796
-8955
9506
-471
8175
-2067
129
2710
3983
-6139
9513
5498
-3339
8529
7241
3385
1188
-8459
-8876
9301
1811
6018
1074
6132
3475
6749
-4802
-7874
-5644
9037
837
-6635
-3069
3923
3596
-7146
9173
-1952
5010
-4688
7733
-4060
3544
9906
2947
2793
-4533
-7525
-6062
-4050
-2301
-7429
-7426
7424
-2564
4427
3635
-6982
-8989
5016
-2879
244
213
4834
599
-641
-1390
40
-9134
-4182
-6508
7885
-7002
-5271
9909
3144
7795
5092
8939
-2098
-2731
-6388
259
-4060
444
-3453
-2107
-6541
-5827
-8029
99
-5633
6566
-3701
-8512
8645
-8591
9379
2002
-1358
-9341
3953
-7919
-8112
-9518
1909
-163
-3337
3523
5842
8692
-3416
4162
605
-4040
-9396
-3602
-1876
-4481
2522
8439
3072
2672
-7832
3007
-4909
3910
9514
-2865
7124
7314
-4235
6899
-6981
3153
1193
-7200
-1807
790
2593
9335
-3381
5918
4069
-4668
5508
-4491
7232
6640
-3817
-1561
5798
2118
-2578
592
-3822
-145
6769
-5235
6550
-6595
4887
-1448
-9946
-2155
-3733
-81
-7161
304
3154
5050
-2091
-2230
130
8731
-5005
1039
-6292
5268
-43
-1790
-7677
8363
1097
-2212
1176
405
2748
-1754
6140
59
-8928
-6369
1616
3737
-9500
-4297
-6024
-1235
-334
742
-851
-1876
-911
-8461
-5969
-373
-4124
-6864
-1375
-1855
-154
-8814
-4228
5133
3249
8451
200
-6055
-1098
-9540
3839
-3069
154
878
1249
-1894
7984
-6543
1875
7044
-7057
9169
7800
4944
-5926
2713
-125
-2353
-4993
9664
-891
-6787
-6082
-2138
-6748
-1918
970
-156
5224
4065
-79
-5171
2044
395
-5465
-467
970
744
-8385
-9030
-366
6606
1436
-2052
-1191
7794
-6942
1983
3463
-5710
-8648
9669
4089
-2615
3456
-3354
-1498
-1255
9552
-5137
-1659
-2992
-2888
2104
-1567
5004
-5809
7686
-8836
6630
2789
1389
-8071
-4470
-3195
7053
4942
-7846
4455
-3835
4071
-4758
-4833
32
9747
-2979
-3400
-4002
-1326
4434
-7961
4317
-6276
8928
-1415
4599
-3524
4911
6596
5291
-6572
1999
2093
-4643
8607
7078
5072
3725
-4812
7571
-4703
4428
-624
-7194
-281
2938
6988
3385
-3834
302
4019
-8037
5680
-8514
1667
-6962
-1630
2858
6159
-4563
-385
-2874
6556
-7874
-5574
-4632
-1235
5546
-857
566
8980
-8531
8326
-3606
-6666
-1355
-3839
3839
8180
-9149
-2691
5443
-6259
7498
966
-374
3778
-9308
-5607
2301
9285
4739
1718
-9910
-1560
6335
-5477
-4440
-6666
6388
-5283
-9653
2598
4160
749
-7991
3424
-1893
-2645
7951
-1878
-5685
-6528
-8831
9348
1219
-6897
-8543
4435
-5432
-5689
2520
-4040
9513
-6090
-9158
595
-3656
-7073
-9831
-1288
-6148
3392
-6595
506
4120
-6340
8979
-4297
-4260
3029
1271
8439
1164
-509
-8043
7832
-9380
8469
1522
7817
-1068
9289
4653
-5853
-2246
2447
-8262
9309
-967
6596
3409
-9565
-3892
1592
8403
-3487
5128
-3986
4160
7829
-3749
-7319
-9946
-264
9049
-3598
2710
4914
9062
-1640
1513
-9090
-1563
6231
-8385
-1043
6841
837
-5051
-6222
-6030
4315
4079
-334
-7560
-6251
7843
307
3814
3617
-6717
-7003
1362
2565
340
6584
-478
-1167
-4742
8908
-1008
-2184
8298
8656
1174
8811
-8896
-2271
-7623
-3234
8175
4478
-2870
6853
5389
119
-8888
515
-3182
267
4071
-4073
-1952
4701
7419
-1229
-2460
-5435
7282
8036
-5435
-612
9454
3796
9394
8039
1520
4980
9747
7610
-283
-4629
-2286
4944
14
6752
-2556
219
2748
-344
1291
4550
-1915
3611
4793
-5373
8811
4990
595
-4064
-543
-3333
2855
-4403
6092
8854
-1727
-2932
-2155
3498
-8574
8868
3607
7683
6765
9502
-2772
6483
185
-1623
3323
-6460
6823
4160
104
-3982
2
267
-8219
165
5469
-9128
-9168
-3822
-6167
-5503
-8450
5735
8790
5393
1926
203
-1938
-5829
4741
-4366
6470
-5680
2002
-7936
-2356
9180
7850
-1972
-7491
-3942
5522
-6055
955
617
-3740
-2224
3406
6772
1343
3653
-1626
-4695
-3301
-7255
417
-5133
-1555
-6781
4220
1824
-8719
-185
-1680
970
1995
3304
-1762
-3469
6931
-3234
8111
-3511
-3598
8536
-8486
9104
-7215
-4116
6556
-9601
7922
-808
-5132
2748
4069
-8195
-4391
-512
-6827
-4430
1803
8734
-3495
8295
-8881
-8945
-9753
-9425
-3791
-1235
1122
540
346
-5853
5698
9343
1774
6154
-9852
-7623
2672
2673
2029
8364
9580
1250
7836
-7942
5035
8731
-8199
-7862
-6967
-3868
6699
5350
-8264
5475
-8650
6300
8607
9049
-7058
9733
-9084
8469
-3990
-5073
-3429
2447
3811
-4174
3491
-4773
4942
-3413
1914
-4857
9938
-8520
7419
6516
-6195
3629
4777
1398
-2694
3705
-3868
8709
9592
-5704
-8960
-5844
8132
3705
2296
7813
913
-483
-7851
974
-1834
-5551
-4365
-5248
-8188
4219
-5689
6451
-7123
5081
-9925
-8554
-6808
-6827
7305
1200
-5288
7861
9049
1150
-2669
-7906
5609
3178
-380
-2694
8805
9620
-9473
-3306
1631
-9955
3648
-2632
5719
-9457
-4167
-8420
-2356
6648
7376
-6822
-8686
8298
1764
4427
9680
-7602
3906
-948
-4678
-3214
-3937
3237
2185
4435
-1192
-5754
5127
212
9960
-273
-1060
784
7483
7371
-5853
-8313
-8996
-5137
-3905
-2698
-6958
-3000
1793
-4800
-2229
-2256
4547
-3863
369
1191
-3064
-2998
1080
-6300
-2504
-2308
-9479
-5522
-851
8289
-606
6642
-8025
8414
-3916
-7769
9780
-9898
-4824
6425
6088
-5137
-7793
3339
7767
-5976
-2391
7854
-1447
-4262
3237
-1989
4444
4666
85
8809
7531
-9833
4329
9885
810
-2184
-4132
944
2223
-8418
-5066
8400
3338
-5407
-9771
436
-2671
-4385
-1125
9642
93
4569
8515
4904
3079
-8019
-1713
8459
6501
1523
377
1053
3538
-6625
-5934
-5785
-2682
5755
2192
-8543
-7716
1855
-7832
4285
1388
1768
-3498
-6384
-5752
-7932
-2575
141
-8388
-8043
5291
-4361
2848
-2992
5941
7452
1150
1475
1840
-322
9081
228
-3924
-3855
-6815
3857
-2250
1468
-205
-1362
340
-8842
-8014
-8009
-9308
9263
6468
-1623
8298
-7677
1439
158
4175
3129
-9498
-5853
1775
5155
130
3872
-2787
-623
400
7980
-8963
129
3385
-3499
-745
1824
2510
-4629
3390
7445
891
-9873
-9155
8212
7597
9475
5042
9197
-46
-4367
4797
-3863
-8927
-759
1072
-143
-7614
3539
-6186
5119
236
4747
-5937
3336
-353
-6964
2713
3648
9970
-1856
-5678
-1108
-9742
-7179
-6212
5502
9583
-967
-9432
-9786
-422
-4694
3623
9560
-5891
-900
-7254
-8702
-3803
1731
9123
-4958
3629
1150
3245
-1187
8132
-3333
3954
-9940
-7562
5322
-931
8518
2967
-9455
-926
-967
1475
3540
-8606
-9964
-6735
-7157
8102
7413
3596
7178
1411
3250
9366
-1278
4201
-1278
3202
-2597
8268
-8625
-3553
1348
-2488
-3863
-6115
6750
-9303
-3495
-7771
1130
-905
9909
-762
-7180
-9371
-2390
6467
-6822
3769
-609
5153
-1650
6962
-6709
9023
8341
-7375
-9773
-6208
7885
-9918
8915
1714
299
-3323
4281
-1259
-6086
6505
5798
225
1983
-60
2759
3196
-5650
4320
1616
4604
-6197
4547
7698
-1927
379
9575
1082
1247
-3279
-3817
-7405
8435
327
-1900
-9983
834
3896
-3509
-9950
2527
6569
2986
8758
-857
-4234
4507
646
-7825
8066
-7398
-3119
-4412
4848
-101
3784
1765
-7375
-8870
-6318
-3884
7017
-9341
7582
-1182
9698
1354
7481
6866
8781
9473
-5819
-7194
981
1889
-5844
7178
-1636
5534
2098
-7179
878
-5396
7051
8143
-8843
-8655
-4221
-4657
-1657
-2310
2598
-165
607
4674
5645
-2242
-3182
-8454
2402
-9562
7883
-4403
-8087
-4056
5794
6513
3942
1357
1229
3537
-2094
-1731
4275
2665
1795
5840
-4742
5354
1883
2473
-5745
-3160
-7602
7378
4408
9985
-730
8855
1040
-4384
8658
7189
-3803
6660
643
4752
-1856
3910
-7004
-8469
3852
2249
-9129
4688
-7027
-2243
7282
1462
-9997
9897
6353
921
-1494
-9994
-6982
7084
-6893
2576
6043
9362
6979
-9080
3097
4567
-3142
2713
-7736
-9706
-556
-4322
-8506
5756
4201
4304
221
-5064
-1561
-8514
7160
-5420
6794
-4657
9348
481
-8234
-9718
2149
2961
2212
-9108
1040
-878
-8391
937
1965
-4628
8790
-5969
3012
2709
-8457
-4064
7100
8132
-7003
-948
-6666
-5171
-740
-4409
-4157
-712
-1375
5016
1573
-8084
4400
8689
6255
-9522
-8084
3632
8189
410
-7442
2006
-900
-7510
5
-9241
5418
-1344
-7096
3003
9808
-4697
4157
5306
8615
6912
-3975
8361
8675
2669
-1434
-9787
6427
3314
6352
1786
-3987
-4911
-691
-3006
-5407
-2591
-2005
-5149
1719
4935
7538
4706
8822
-9134
7313
-7640
1292
-8400
7918
4089
9348
6511
1523
-2119
7552
4928
3421
-9148
-2013
-8206
8270
5109
556
-9606
41
2001
-6620
230
4547
-2865
8579
-8302
3316
8669
-1649
7094
3469
-8286
-1200
-4715
-4611
-3343
-7032
839
1376
3725
-322
-9394
7073
1764
-3791
4602
8670
-2033
-7491
974
9752
-8746
-2645
-9445
-9904
-8138
-7668
-3821
-3677
2744
-4915
-2077
8743
-5423
-5685
3128
766
-2079
-3466
-7157
7423
4818
-9308
-632
-8455
4230
-9486
-4140
5481
8999
8517
6465
-4110
6624
-3106
-9243
2862
6855
2055
-6191
9231
-8437
-80
-2005
8105
-1579
-3525
2054
4547
8482
6943
8356
-5217
5008
3551
-6543
-1129
6468
4286
5184
-4238
-1493
8790
5004
-8288
7953
-2234
2686
4483
6018
-5069
-1160
-1245
157
-952
-5852
3230
3055
8232
9104
8673
-1899
9564
5426
-8828
1922
5646
4037
9893
-6300
8276
-2585
1656
2890
-2913
-849
8280
-745
6487
-8171
-6332
-1697
5412
-9214
-8826
5941
7091
2082
4187
-6369
7331
6898
-9795
230
-959
2969
-8116
475
-2720
-6753
-5502
1059
5092
5131
-390
5714
-6318
-7861
7884
9461
98
9348
-6009
7951
6431
-8140
7229
7589
-6756
-500
1751
6912
-7558
4990
-3354
1974
2576
-8331
-3140
5603
-2086
540
-8868
4818
-205
-1651
5040
2269
3839
3540
1435
-8330
-7683
-2597
-7003
2212
-2677
9143
-2723
-8710
2104
-4622
3343
8521
-1730
-7781
-3296
8947
-741
6853
-9479
-2102
-2669
-2427
6139
9485
-3950
-3413
-5997
-7560
5992
-1591
-5651
827
-4961
5834
4452
1554
4944
7119
4621
3231
-6669
9229
5456
8201
-28
1727
430
8219
3051
-1415
405
-2473
6004
4082
-2042
-4489
-7683
-1375
-4577
6648
-7402
1112
3187
-3803
-1576
-1563
-436
-5756
4578
319
1840
-8366
-4902
-4384
3474
267
9030
-3119
4888
468
-7847
-3036
8039
1173
2211
-4011
-1956
-1912
4653
-7861
-8204
1702
3890
3648
932
-5137
1154
-3234
3752
-6245
9348
-3632
2212
-4202
8414
-8459
70
-3955
1019
-5540
273
680
-8344
6355
-3848
1462
-8303
8120
-4918
-3808
3596
-3932
-3306
5548
2001
5082
-9230
-3791
-1240
-6640
-874
-4637
-9415
-7886
773
-5193
4318
-3216
-3152
-6664
-5809
9284
-9461
7751
2024
-1555
-9452
-9102
3079
1051
-3120
-5773
-4119
6219
-5831
-5596
1155
5951
-4781
3537
-7037
8905
-6645
-6185
-4426
9111
-6186
4644
3279
5371
3368
6763
8640
-8908
-807
-3241
7190
3927
996
-2876
-7981
784
-2760
-7858
6685
-3525
-2119
7846
9335
2981
9966
4281
2685
7378
-7211
-2025
-5845
5148
2473
8429
1393
-4355
7319
245
1390
1387
-6730
5755
-6595
-4160
5619
3682
-4693
-7494
6652
-5651
1393
-7274
8851
-2148
790
4337
3463
9118
-6369
4546
-2550
775
-1560
5548
-2591
-4783
-6922
1616
7150
8562
-8295
5794
-1592
-9952
-7077
1717
8009
1462
5905
-1527
7813
-9875
1401
4284
5644
-8782
6358
8949
-6143
-2869
-2926
3094
-4987
-1963
-2454
-3803
9520
1689
5227
-8962
-4024
-4018
-1467
-4933
-2328
-6815
-4408
9485
5510
1320
856
4766
-2382
9498
-9303
9225
-3127
1320
-979
6683
6421
-9940
-8865
-3279
1039
8607
7740
1263
6797
-1234
327
-9581
680
-8352
2300
3213
-3357
-8084
-1248
-9505
-3375
9477
-491
-1253
-3306
2261
-2752
-6980
-2471
-9730
-5773
-252
-4515
7273
6717
-3598
-4852
-80
4980
-6377
-277
-1304
-4412
1445
-5934
-3671
-1794
2060
9669
-9642
-979
7703
555
-9532
3442
7388
-1710
2407
-7180
7674
-3984
9239
773
-1755
2117
-8896
4599
-505
-443
-2049
-5343
5659
9822
-5586
-8364
2922
6767
-2779
-8388
-8068
-4915
-7345
6077
-4238
1029
-3176
7914
28
-7231
-5313
-6873
8683
-7932
5899
8848
1824
-1249
-9866
8719
8740
3629
9473
8216
-4193
-7428
-7825
-2065
839
3965
2515
143
-7683
-6942
7371
-6301
5016
-1970
6851
-2077
2951
-266
-1598
-5780
-9977
-7774
-342
-6275
4651
6967
1932
-4222
4424
1799
2857
3572
5840
-86
-4804
-1420
-5640
5893
236
-2556
-16
-5314
-3419
3801
2006
5588
-6251
-7265
6052
-7199
-5868
-7876
8979
-423
-8995
-2160
-4247
5
-5032
4062
6919
-9414
937
-3694
-3441
7418
39
8168
-4478
-7731
8830
-8606
3277
-380
7048
377
512
2981
-743
-4342
-8040
-3553
-7893
8965
6016
9450
4082
-1899
-8810
8190
-7534
-3638
4301
-1129
4534
-9887
-6474
4834
-3574
-3003
1263
-5145
8654
-10000
-3069
-8234
-8932
-5325
-8678
9184
9348
7701
-3953
-1917
3470
9971
-1836
-7552
-4736
8898
-675
9834
-6763
157
216
1404
1502
-8238
-3414
-5511
8579
-7402
2218
-9128
-5607
4736
-2230
-5462
-9085
-5094
6104
1435
-9427
-8938
4910
-420
-2308
5186
-5864
1436
-566
-3587
8743
6401
253
-5333
3133
-832
-5852
5513
8341
1637
9611
-9875
2527
-7942
4313
4083
4005
-76
7102
-521
4305
-9357
8297
-8340
8091
-7933
2886
-8805
4803
-6055
1592
-7759
1167
3269
677
99
6241
-8455
-8973
2800
-938
-6818
-9806
6467
-2581
7538
1414
70
9664
-8746
-6373
-6983
1743
2603
4887
-7016
-6992
7774
-9420
2439
-6454
-6413
371
4004
-7614
-4023
-665
5842
8669
9108
9653
1799
-9158
-2254
-8159
-6483
-9473
-5985
9111
-7661
-6362
7679
3178
-9238
-8629
-8266
-6885
-7296
-8626
-2691
5153
-8227
-1899
4944
1787
3195
-1088
3791
-8499
-1854
-8998
3542
4281
9737
3942
8713
5301
-4800
-6905
9494
3751
-434
-99
1915
3560
6970
2152
8207
-2034
-7984
-9587
-975
-3623
-6666
-6274
-1556
-7471
8968
-3839
-6274
1222
7213
4715
5609
1291
-9055
7841
6343
-9779
4135
5562
4406
7751
-2198
536
-3048
-7282
452
-2736
7885
6214
-7625
5079
-8108
-5137
834
-8014
-9938
-8782
-2982
-1560
4281
-719
698
3392
-8656
9966
5941
-9562
2793
4446
8743
9665
9979
-3856
-1462
-7893
-5002
-1059
-4632
7833
-5709
8744
-4758
-3797
-1952
135
-197
9366
2805
-6245
-8278
-848
8731
-316
6920
4069
3814
-7644
7689
2496
-7436
5546
-8623
-6840
9658
-3615
-7095
621
-3701
9659
-6905
-4140
-4589
4716
-8218
-612
3985
9495
-7888
3572
4860
8861
1114
-2913
-794
-1898
-2274
-7535
9049
7110
-4096
6144
-714
-3250
-1379
6522
6143
-4110
1581
7052
-4132
7658
4329
7128
2590
2459
9498
-8874
2092
-1547
185
-6913
-9803
5842
-9821
7797
8212
5701
-8682
2398
9058
-5967
4501
4579
-3147
8621
7813
-3920
7742
5155
-1686
-2121
856
4981
-4056
3195
-3000
-3655
-5642
-762
7935
-9455
-5880
-6807
2725
9104
2626
-6253
3859
-6696
-5013
6132
4446
-1129
-252
-947
-3932
566
8564
8681
-2202
2004
-6276
-3906
7096
-9371
-496
9966
3470
558
-7658
7918
-3760
4501
-4231
6062
-1375
-2285
-7425
3249
-381
-5906
-937
6882
-4952
-4434
-5275
-3152
-5091
-6940
-1799
5941
4256
-9341
-6806
-9165
1849
9466
-4654
8611
-5435
-7347
-3113
-2246
-543
252
6824
35
1111
-2431
-5636
1022
-6977
-4517
2853
-4808
8859
-4077
2710
-5133
-2759
-6379
6457
8675
-1989
-4227
1414
9454
401
-7847
-9810
5511
-2686
-7005
-647
8290
191
-95
-4152
-7913
4793
6855
9514
-6116
-558
-6419
-4047
4129
3353
-3275
1019
-8803
-4786
3463
5036
-4757
-543
7613
4980
4256
-8906
-4894
5309
4076
-7487
7166
-624
-7001
6853
-4403
-7281
1332
-4921
-6185
-1105
8654
-7059
344
5966
-8089
-3043
3127
-6703
7228
-171
8214
-8219
-6212
6944
-857
-1801
7259
-6915
8683
5254
-3152
8372
-1950
-9505
6668
6340
7939
5153
3537
-6595
-2272
2178
8605
6922
-8554
-8771
-2737
-6676
9714
7499
-8506
7883
-8522
-214
-6434
4253
-8208
-9380
-5980
410
5036
-3241
7658
749
-794
6411
8584
-1339
-5153
9688
-5283
338
-9188
-4039
4580
-2795
-1060
-9582
-4703
-6034
-6208
971
3830
-7677
-5705
9665
-491
8440
3279
9363
-8123
-5132
-1730
2845
9203
8802
-5776
-8718
-5914
-2742
2343
4766
7976
3854
9023
3646
5894
2603
-4078
-4632
1354
2887
6802
-5747
-4918
8854
-1675
1264
9822
2606
-900
-1819
2419
-9599
-6098
6500
2819
-2243
-7913
-7644
-8676
2256
-3905
5433
3269
3737
3405
7751
285
8869
403
-7534
3638
-7933
283
599
-6988
-3012
-4485
8120
-5736
-3808
9454
-7871
3670
1747
3214
4441
129
-1436
8851
8800
842
2966
3178
-8591
-4081
1044
891
-5137
-3822
-249
-1702
-1651
-9297
3392
-6140
989
8673
5150
6539
-740
-331
-4949
-9828
5016
9257
-9678
-7690
346
4172
1522
6046
-5233
5011
786
-7283
-5344
-3473
9150
5572
2374
7538
4123
-1456
-5147
-3243
-1347
1567
-7160
262
-6776
-1071
-6487
-891
-6640
-7782
1787
8811
-5619
-5539
7698
-8497
9104
9946
-1142
-6751
-5633
6819
9943
-9478
-8138
-1488
7820
8858
-4406
8313
-4240
-8831
-8116
6422
-6543
-5864
-2677
-2169
1126
3302
-7509
-2746
2482
6742
1077
4693
4220
9966
-9653
-3625
-223
4996
8827
-9579
-6485
-4488
8495
-5384
1607
1809
6675
8226
6114
-5006
-3584
-1731
-3375
5782
-9161
-9691
6869
-4157
-5009
876
-696
-7003
5472
-67
-2947
-4132
-7809
-2036
8210
-4952
1482
-1378
6071
7199
4224
-1088
-4117
-2119
-7574
-4888
2897
7817
9397
-7175
-5417
-1916
-4134
9619
-8373
3538
-4786
493
-5651
-8646
1749
8193
1485
7993
2361
7791
3254
-2866
-5853
4924
4904
9483
-9964
-9997
-2576
4716
4707
232
-1646
5153
-265
-5769
-947
2472
-728
7730
8740
6702
-8815
3768
-3419
-3051
8091
-1321
7713
7198
-5609
6576
-2096
-2306
9032
-1918
1789
4056
5358
-6706
-5612
-9670
1155
9417
6043
-190
4766
-1731
-394
-529
7485
7567
8474
5539
-4310
8383
8790
4692
-5645
5508
1487
4135
4224
969
2998
7843
-4843
7661
1268
2306
7621
-2155
4797
-6022
5502
-2880
-694
706
2658
-9579
5840
876
-9310
1393
6911
3049
3580
-3822
8575
-4907
4223
-8843
4489
74
7813
-8025
-138
8368
-3667
4569
6581
-5283
-2149
-4149
-2770
8455
-2111
-2753
2374
8189
2068
4382
-9737
2714
-1283
5126
2539
9954
3026
-9952
8801
-4478
-4368
-2778
1518
-3563
5992
3474
-2479
7542
151
-1875
154
8186
1897
7432
-3189
4293
-4741
7498
9816
-1191
-763
-979
-6696
1858
8112
-9583
8600
-4670
-3822
7335
-7016
-310
1576
-6547
2327
6851
706
9798
-6850
6296
-5334
-3296
-7005
6219
-2482
1072
1074
1974
2940
2533
610
7297
2982
4541
-7739
3494
3842
1465
9747
-1834
-1555
-3171
-2158
-8459
-5818
-4359
6921
-1049
4201
8003
9413
338
-9640
3249
3012
6425
-1700
-7545
-52
8360
5288
-2064
-358
-6285
-7681
5294
5539
7226
-1401
6698
-5002
6062
-7346
9907
-1687
1513
6219
-8526
-4760
1162
4097
-7537
2301
-6839
-1022
-8764
-7467
4599
6288
7442
1199
-3399
-4134
-7019
2772
7730
-2356
6666
2562
5519
4219
3007
6831
7376
-661
-1344
-6304
-5091
2551
9727
3455
9000
9846
-2996
1705
-7536
9859
266
-8982
2225
-6855
1549
-8469
50
-3618
-9349
-6578
-7427
1342
-6917
-3913
1166
-609
9681
-9569
2211
-3306
9394
-8236
-9883
2802
-1033
-7146
-9049
-3630
-2052
1609
2562
-1351
-317
-3176
-5609
-8676
1513
-9134
6219
-5515
-1125
8371
-3583
-3152
-7501
-5618
2452
-9562
8273
7189
-1379
-3761
4083
-6772
-2272
-2577
7577
1027
-4409
-9604
2462
-1173
7048
2967
3032
4069
-7411
2152
-4153
93
7656
-2892
4942
2541
246
-2241
9664
6182
1023
-6443
6763
1075
-6474
-4911
3637
9733
-9920
4741
9056
-2519
2725
-9776
2360
8254
-9343
-5129
2075
-6395
3765
9747
5548
1452
-5849
840
-4244
-1952
649
-5359
5607
-8400
6561
-1253
3721
-1687
3945
1915
-6984
-252
-9752
-3305
7459
-8716
-9127
-8460
7413
2575
-8108
291
-8868
153
913
-1161
-8786
3011
-8405
6154
2026
7106
8513
8456
7655
-7114
-4271
-1248
3977
1858
714
-5435
-8714
-7040
2235
7813
-812
3637
5079
8625
216
8853
1773
2327
-3773
-3584
3464
-1680
3484
-2434
5708
123
3511
8451
-1552
2435
-8548
-3127
-6915
-8171
5265
8817
1699
-3531
541
-4488
6114
5126
-7786
7538
7582
4473
8492
-1913
-5137
1855
7499
-2992
2029
-2489
5050
3629
3537
2717
6465
2939
3689
9870
-1694
-8281
8405
1826
-2286
-4952
-1494
4342
-304
8086
2847
-8454
-3418
-578
-8112
-7979
-6621
5109
7819
1835
-6853
2866
44
4603
-7293
-1560
-6852
135
-8988
4583
-4227
1437
-3658
380
-5447
6791
4590
-7475
9983
-6969
5268
5574
-8181
1616
-6238
8025
-3028
-8718
-646
310
-3850
-5522
8325
3573
-8872
593
2940
2070
4292
-343
-422
3011
-6941
7558
-1082
-2859
5799
4110
-9871
9835
-9369
4911
-3444
876
5580
-335
-1250
3026
-9992
4703
-6109
9180
3705
-8333
-4830
-914
-9971
7971
-6663
-5591
1366
3041
2296
971
-7533
-8340
-6654
-2949
-7180
4285
4160
-3234
-8998
3859
-1246
7390
2919
-6507
9749
-9442
-1243
-8705
-1680
9350
5076
3997
-2962
3469
889
3913
5808
2606
7435
-7904
-2988
2845
-3327
219
-2290
1770
2964
-6441
5371
1609
4609
7713
5142
9421
-4384
-4132
-5159
3646
5556
259
1390
9651
9160
-7560
5580
-638
-2445
883
7202
-9992
-506
-9587
-3862
-3096
-3538
-6024
4427
4329
-4800
-8700
3510
-6925
333
-8191
-9531
7609
-4319
-693
-3586
-2121
-4598
4641
-4597
8459
-4993
7615
-2820
2016
74
-6278
-1650
5227
-2617
-190
-3289
-8107
9560
-6304
617
-5792
-2397
-4217
5913
-6407
-1486
9520
-4141
7731
-5816
878
2193
-1727
-5231
1863
-3408
9966
9473
-8910
-5341
5444
-1887
-1641
-4572
6880
-6977
647
-4591
-2164
6425
2033
4128
-7200
-4918
-5574
9689
-2970
5436
-1442
3493
-6085
8670
9607
-4193
3237
-8326
9121
-6300
9139
1843
-1776
-4482
-1129
-2471
5352
8315
9316
-1125
-6319
1991
7026
-4270
6792
4236
1138
-9154
-2597
5946
3175
4428
1208
2971
7885
-536
9521
-6146
-1318
-9531
7372
-6347
-8595
-356
-2913
-8820
-3301
-8499
-7653
-5373
-4780
8477
837
2646
-1766
-3142
3843
4179
-8533
-1541
-9267
-718
-8955
-2427
-6413
5525
2336
1347
-1774
-7129
-7525
-4852
-4235
-4067
-3653
-8906
-6104
-6214
-4340
-8352
-4036
-5438
2889
8240
6758
-483
-9141
3058
1330
8968
-9371
-7929
5849
-7936
1267
5148
7707
1790
-5773
-6787
2038
2965
-1049
-8546
-6483
8372
176
-5761
-1799
9607
-1475
-8922
7388
7006
-3587
8756
6358
-8597
9138
8918
-8678
-8161
-6274
8698
1724
245
-6460
-1498
-1369
310
299
-4508
-4281
3859
-9620
970
2865
-2824
5619
9879
3353
-5572
5357
-4852
-9165
-2111
3419
424
-2597
-217
5641
6727
4285
8536
6550
8926
70
7907
6889
7529
4056
6618
-1685
8274
-8038
4701
-975
-1711
7048
-9432
-9155
4797
6312
7797
-5811
-3357
3266
-9279
-511
-1680
-7355
6061
-9137
1264
-9910
4573
577
-2540
-3562
-8907
3309
6880
5494
-4337
9411
-9461
19
9352
-4180
9679
9974
7407
-8591
8459
8781
-4278
-8091
5159
-9888
1191
-2013
7972
-12
-2801
-9583
-7658
-6872
3090
1931
2768
-725
4408
-5248
6388
3638
4065
7158
-7066
-5574
4699
-264
9764
8571
-4876
-4279
2929
8094
6561
2457
-3151
1415
4105
3623
2143
6425
9570
-3151
-1552
1095
-5741
8724
-4322
-6139
-1534
4149
7228
-9850
-3624
-7657
5823
-9946
4941
-3095
-2511
4739
-907
-3228
-572
-2125
9747
-7877
647
7924
-1557
167
879
1726
8469
-8710
-5599
5810
9203
1656
5742
6452
-6739
1883
1354
-8071
7679
6431
5804
-1894
-5514
7695
1664
-1783
-7599
1855
-6027
-988
4779
9809
-1680
6466
-1799
-4673
-6707
-2358
6823
-1105
-4440
-4043
3589
1905
7582
8214
4830
-2526
-4090
6819
7917
-2600
-5764
9613
2187
1393
6331
225
-2451
-374
2418
-3516
-9494
-7878
3528
3274
5265
4887
-4238
-5770
9035
-6786
8941
-5018
1964
6474
-4703
9497
-7926
2779
-8825
-3197
-1270
9184
-5819
7654
5569
-8648
333
-6412
8833
-1289
7366
9407
7128
200
4883
5358
-9887
8308
4946
5109
-9974
-9286
5972
7427
-2229
-3137
3596
4341
-1129
-1498
4675
4946
5481
8144
-9590
4513
236
-7791
8673
-6412
-4383
-3036
8077
-5325
-1270
-4408
-5420
-8472
2472
-6576
-651
-6752
-4850
212
-2917
-4798
6213
-7752
6794
-6956
3839
-8003
-9713
891
-5790
-8039
-1344
1352
7560
4175
7989
-4894
-1192
-3932
1724
2669
8579
5446
-9737
9616
5592
-1025
-6921
-1173
-5139
1073
-9044
815
-6045
143
6295
-1275
-5672
-4823
2404
6992
-134
-5043
-5607
-9050
-6185
-7263
5186
6466
-891
102
2301
-6664
7366
7843
9970
7771
-6376
-9841
8621
589
-3058
-8883
430
3533
3412
-6575
-6640
-810
8780
395
-2270
-2151
4604
6277
3051
-3354
8308
1249
3729
-9429
-7764
-2519
-108
3292
8676
8273
2400
4314
2301
6606
-2604
-4116
3802
3455
104
-9952
-3638
8681
-1135
-8768
-2443
-6153
-578
-4591
8053
-3200
8908
-1280
4941
4417
-5043
8624
-6152
1486
3277
2529
1965
-6359
960
-8263
3383
-3587
6263
-6880
5509
2705
-344
1398
7014
-9660
-7819
-7793
370
-1122
-2790
1417
-3340
-7873
-8720
5778
7691
3336
-7213
1849
-3385
989
9373
-3705
4046
-6711
461
-9601
7386
1473
-8768
-4516
-1492
-3012
522
2228
9681
-7774
4427
-8295
2232
6893
2283
-7603
4489
1003
7040
7468
8775
-7575
3954
-9795
1776
8139
3692
3929
9540
3754
856
4934
-1731
-3625
-5343
1664
-7438
-5645
-8522
-2233
2527
-878
-832
-9264
-2779
-848
-847
-1064
-7675
-4921
-4550
4852
9350
-3051
2429
4547
1364
-9244
3721
-2888
5371
7907
4610
9855
-4320
9134
-4532
8668
2998
-163
-4633
-947
6606
-9598
-4035
346
9407
3784
3958
9658
-218
-307
-164
-1527
-8087
-7089
-6115
4587
363
-1076
-4455
1155
-343
5902
1746
7774
2598
-7655
-1611
8760
6028
-8171
-3142
-7101
-2787
-3381
-9964
-8230
-4620
-6585
4069
1210
-4497
3430
-5147
2092
7070
3682
7100
-5921
-5829
-4800
-9587
-7836
6683
-6508
3373
-8892
3351
-8973
7011
-8144
-134
-1650
2820
9161
-7768
-9498
-1988
3288
3888
-3248
-3108
-780
-6556
1310
3880
4793
-3634
-9378
7432
-9161
5219
-143
6587
5669
-1462
9758
-3352
-1600
-6392
-8736
2958
-5893
3133
8758
4603
-606
-5137
5416
-6925
-7140
-6533
2283
3830
5433
3839
5972
-5449
-4843
3778
8388
7130
4218
-8329
3611
-9196
5291
-6089
3354
3977
-8791
135
9681
-3673
-511
1055
9611
9283
8670
-2990
-5663
555
8270
-6960
-6856
-8276
-2429
-1213
8486
-1842
6143
7764
-366
-8343
-7668
4891
-1833
4571
-1920
-4383
-3791
8507
-9007
-6071
-5129
792
3027
1199
-4368
-2890
3264
-2580
-3304
-8431
-719
6201
-8510
7918
3500
6435
2340
-2334
-1557
724
4829
-409
4531
1530
7694
7946
9520
9896
9905
-1957
-1707
-3113
1915
-8454
-9820
9536
4947
-7771
9023
-878
-8132
3249
-4800
9348
-5137
-211
-5906
-1407
-6379
998
-3632
4580
4224
0
5951
-4950
3826
4049
-6869
818
6606
-7121
-9380
-9678
-7702
1310
7555
1128
""")

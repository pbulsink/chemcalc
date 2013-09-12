#!/usr/bin/env python
import string

raw_tabled = """<tr>
<td>1</td>
<td>H</td>
<td>1.00782503207</td>
<td>99.9885</td>
</tr>
<tr>
<td>2</td>
<td>H</td>
<td>2.0141017778</td>
<td>0.0115</td>
</tr>
<tr>
<td>3</td>
<td>He</td>
<td>3.0160293191</td>
<td>0.000134</td>
</tr>
<tr>
<td>4</td>
<td>He</td>
<td>4.00260325415</td>
<td>99.999866</td>
</tr>
<tr>
<td>6</td>
<td>Li</td>
<td>6.015122795</td>
<td>7.59</td>
</tr>
<tr>
<td>7</td>
<td>Li</td>
<td>7.01600455</td>
<td>92.41</td>
</tr>
<tr>
<td>9</td>
<td>Be</td>
<td>9.0121822</td>
<td>100.00</td>
</tr>
<tr>
<td>10</td>
<td>B</td>
<td>10.0129370</td>
<td>19.9</td>
</tr>
<tr>
<td>11</td>
<td>B</td>
<td>11.0093054</td>
<td>80.1</td>
</tr>
<tr>
<td>12</td>
<td>C</td>
<td>12.0000000</td>
<td>98.93</td>
</tr>
<tr>
<td>13</td>
<td>C</td>
<td>13.0033548378</td>
<td>1.07</td>
</tr>
<tr>
<td>14</td>
<td>N</td>
<td>14.0030740048</td>
<td>99.636</td>
</tr>
<tr>
<td>15</td>
<td>N</td>
<td>15.0001088982</td>
<td>0.364</td>
</tr>
<tr>
<td>16</td>
<td>O</td>
<td>15.99491461956</td>
<td>99.757</td>
</tr>
<tr>
<td>17</td>
<td>O</td>
<td>16.99913170</td>
<td>0.038</td>
</tr>
<tr>
<td>18</td>
<td>O</td>
<td>17.9991610</td>
<td>0.205</td>
</tr>
<tr>
<td>19</td>
<td>F</td>
<td>18.99840322</td>
<td>100.00</td>
</tr>
<tr>
<td>20</td>
<td>Ne</td>
<td>19.9924401754</td>
<td>90.48</td>
</tr>
<tr>
<td>21</td>
<td>Ne</td>
<td>20.99384668</td>
<td>0.27</td>
</tr>
<tr>
<td>22</td>
<td>Ne</td>
<td>21.991385114</td>
<td>9.26</td>
</tr>
<tr>
<td>23</td>
<td>Na</td>
<td>22.9897692809</td>
<td>100.00</td>
</tr>
<tr>
<td>24</td>
<td>Mg</td>
<td>23.985041700</td>
<td>78.99</td>
</tr>
<tr>
<td>25</td>
<td>Mg</td>
<td>24.98583692</td>
<td>10.00</td>
</tr>
<tr>
<td>26</td>
<td>Mg</td>
<td>25.982592929</td>
<td>11.01</td>
</tr>
<tr>
<td>27</td>
<td>Al</td>
<td>26.98153863</td>
<td>100.00</td>
</tr>
<tr>
<td>28</td>
<td>Si</td>
<td>27.9769265325</td>
<td>92.223</td>
</tr>
<tr>
<td>29</td>
<td>Si</td>
<td>28.976494700</td>
<td>4.685</td>
</tr>
<tr>
<td>30</td>
<td>Si</td>
<td>29.97377017</td>
<td>3.092</td>
</tr>
<tr>
<td>31</td>
<td>P</td>
<td>30.97376163</td>
<td>100.00</td>
</tr>
<tr>
<td>32</td>
<td>S</td>
<td>31.97207100</td>
<td>94.99</td>
</tr>
<tr>
<td>33</td>
<td>S</td>
<td>32.97145876</td>
<td>0.75</td>
</tr>
<tr>
<td>34</td>
<td>S</td>
<td>33.96786690</td>
<td>4.25</td>
</tr>
<tr>
<td>36</td>
<td>S</td>
<td>35.96708076</td>
<td>0.01</td>
</tr>
<tr>
<td>35</td>
<td>Cl</td>
<td>34.96885268</td>
<td>75.76</td>
</tr>
<tr>
<td>37</td>
<td>Cl</td>
<td>36.96590259</td>
<td>24.24</td>
</tr>
<tr>
<td>36</td>
<td>Ar</td>
<td>35.967545106</td>
<td>0.3365</td>
</tr>
<tr>
<td>38</td>
<td>Ar</td>
<td>37.9627324</td>
<td>0.0632</td>
</tr>
<tr>
<td>40</td>
<td>Ar</td>
<td>39.9623831225</td>
<td>99.6003</td>
</tr>
<tr>
<td>39</td>
<td>K</td>
<td>38.96370668</td>
<td>93.2581</td>
</tr>
<tr>
<td>40</td>
<td>K</td>
<td>39.96399848</td>
<td>0.0117</td>
</tr>
<tr>
<td>41</td>
<td>K</td>
<td>40.96182576</td>
<td>6.7302</td>
</tr>
<tr>
<td>40</td>
<td>Ca</td>
<td>39.96259098</td>
<td>96.941</td>
</tr>
<tr>
<td>42</td>
<td>Ca</td>
<td>41.95861801</td>
<td>0.647</td>
</tr>
<tr>
<td>43</td>
<td>Ca</td>
<td>42.9587666</td>
<td>0.135</td>
</tr>
<tr>
<td>44</td>
<td>Ca</td>
<td>43.9554841</td>
<td>2.086</td>
</tr>
<tr>
<td>46</td>
<td>Ca</td>
<td>45.9536926</td>
<td>0.004</td>
</tr>
<tr>
<td>48</td>
<td>Ca</td>
<td>47.952534</td>
<td>0.187</td>
</tr>
<tr>
<td>45</td>
<td>Sc</td>
<td>44.9559119</td>
<td>100.00</td>
</tr>
<tr>
<td>46</td>
<td>Ti</td>
<td>45.952631</td>
<td>8.25</td>
</tr>
<tr>
<td>47</td>
<td>Ti</td>
<td>46.951763</td>
<td>7.44</td>
</tr>
<tr>
<td>48</td>
<td>Ti</td>
<td>47.9479463</td>
<td>73.72</td>
</tr>
<tr>
<td>49</td>
<td>Ti</td>
<td>48.9478700</td>
<td>5.41</td>
</tr>
<tr>
<td>50</td>
<td>Ti</td>
<td>49.9447912</td>
<td>5.18</td>
</tr>
<tr>
<td>50</td>
<td>V</td>
<td>49.9471585</td>
<td>0.250</td>
</tr>
<tr>
<td>51</td>
<td>V</td>
<td>50.9439595</td>
<td>99.750</td>
</tr>
<tr>
<td>50</td>
<td>Cr</td>
<td>49.9460442</td>
<td>4.345</td>
</tr>
<tr>
<td>52</td>
<td>Cr</td>
<td>51.9405075</td>
<td>83.789</td>
</tr>
<tr>
<td>53</td>
<td>Cr</td>
<td>52.9406494</td>
<td>9.501</td>
</tr>
<tr>
<td>54</td>
<td>Cr</td>
<td>53.9388804</td>
<td>2.365</td>
</tr>
<tr>
<td>55</td>
<td>Mn</td>
<td>54.9380451</td>
<td>100.00</td>
</tr>
<tr>
<td>54</td>
<td>Fe</td>
<td>53.9396105</td>
<td>5.845</td>
</tr>
<tr>
<td>56</td>
<td>Fe</td>
<td>55.9349375</td>
<td>91.754</td>
</tr>
<tr>
<td>57</td>
<td>Fe</td>
<td>56.9353940</td>
<td>2.119</td>
</tr>
<tr>
<td>58</td>
<td>Fe</td>
<td>57.9332756</td>
<td>0.282</td>
</tr>
<tr>
<td>59</td>
<td>Co</td>
<td>58.9331950</td>
<td>100.00</td>
</tr>
<tr>
<td>58</td>
<td>Ni</td>
<td>57.9353429</td>
<td>68.0769</td>
</tr>
<tr>
<td>60</td>
<td>Ni</td>
<td>59.9307864</td>
<td>26.2231</td>
</tr>
<tr>
<td>61</td>
<td>Ni</td>
<td>60.9310560</td>
<td>1.1399</td>
</tr>
<tr>
<td>62</td>
<td>Ni</td>
<td>61.9283451</td>
<td>3.6345</td>
</tr>
<tr>
<td>64</td>
<td>Ni</td>
<td>63.9279660</td>
<td>0.9256</td>
</tr>
<tr>
<td>63</td>
<td>Cu</td>
<td>96.9295975</td>
<td>69.15</td>
</tr>
<tr>
<td>65</td>
<td>Cu</td>
<td>64.9277895</td>
<td>30.86</td>
</tr>
<tr>
<td>64</td>
<td>Zn</td>
<td>63.9291422</td>
<td>48.268</td>
</tr>
<tr>
<td>66</td>
<td>Zn</td>
<td>65.9260334</td>
<td>27.975</td>
</tr>
<tr>
<td>67</td>
<td>Zn</td>
<td>66.9271273</td>
<td>4.102</td>
</tr>
<tr>
<td>68</td>
<td>Zn</td>
<td>67.9248442</td>
<td>19.024</td>
</tr>
<tr>
<td>70</td>
<td>Zn</td>
<td>69.9253193</td>
<td>0.631</td>
</tr>
<tr>
<td>69</td>
<td>Ga</td>
<td>68.9255736</td>
<td>60.108</td>
</tr>
<tr>
<td>71</td>
<td>Ga</td>
<td>70.9247013</td>
<td>39.892</td>
</tr>
<tr>
<td>70</td>
<td>Ge</td>
<td>69.924247</td>
<td>20.38</td>
</tr>
<tr>
<td>72</td>
<td>Ge</td>
<td>71.9220758</td>
<td>27.31</td>
</tr>
<tr>
<td>73</td>
<td>Ge</td>
<td>72.9234589</td>
<td>7.76</td>
</tr>
<tr>
<td>74</td>
<td>Ge</td>
<td>73.9211778</td>
<td>36.72</td>
</tr>
<tr>
<td>76</td>
<td>Ge</td>
<td>75.9214026</td>
<td>7.83</td>
</tr>
<tr>
<td>75</td>
<td>As</td>
<td>74.9215965</td>
<td>100.00</td>
</tr>
<tr>
<td>74</td>
<td>Se</td>
<td>73.9224764</td>
<td>0.89</td>
</tr>
<tr>
<td>76</td>
<td>Se</td>
<td>75.9192136</td>
<td>9.37</td>
</tr>
<tr>
<td>77</td>
<td>Se</td>
<td>76.9199140</td>
<td>7.63</td>
</tr>
<tr>
<td>78</td>
<td>Se</td>
<td>77.9173091</td>
<td>23.77</td>
</tr>
<tr>
<td>80</td>
<td>Se</td>
<td>79.9165213</td>
<td>49.61</td>
</tr>
<tr>
<td>82</td>
<td>Se</td>
<td>81.916994</td>
<td>8.73</td>
</tr>
<tr>
<td>79</td>
<td>Br</td>
<td>78.9183371</td>
<td>50.69</td>
</tr>
<tr>
<td>81</td>
<td>Br</td>
<td>80.9162906</td>
<td>49.31</td>
</tr>
<tr>
<td>78</td>
<td>Kr</td>
<td>77.9203648</td>
<td>0.355</td>
</tr>
<tr>
<td>80</td>
<td>Kr</td>
<td>79.9163790</td>
<td>2.286</td>
</tr>
<tr>
<td>82</td>
<td>Kr</td>
<td>81.9134836</td>
<td>11.593</td>
</tr>
<tr>
<td>83</td>
<td>Kr</td>
<td>82.914136</td>
<td>11.500</td>
</tr>
<tr>
<td>84</td>
<td>Kr</td>
<td>83.911507</td>
<td>56.987</td>
</tr>
<tr>
<td>86</td>
<td>Kr</td>
<td>85.91061073</td>
<td>17.279</td>
</tr>
<tr>
<td>85</td>
<td>Rb</td>
<td>84.911789738</td>
<td>72.17</td>
</tr>
<tr>
<td>87</td>
<td>Rb</td>
<td>86.909180527</td>
<td>27.83</td>
</tr>
<tr>
<td>84</td>
<td>Sr</td>
<td>83.913425</td>
<td>0.56</td>
</tr>
<tr>
<td>86</td>
<td>Sr</td>
<td>85.9092602</td>
<td>9.86</td>
</tr>
<tr>
<td>87</td>
<td>Sr</td>
<td>86.9088771</td>
<td>7.00</td>
</tr>
<tr>
<td>88</td>
<td>Sr</td>
<td>87.9056121</td>
<td>82.58</td>
</tr>
<tr>
<td>89</td>
<td>Y</td>
<td>88.9058483</td>
<td>100.00</td>
</tr>
<tr>
<td>90</td>
<td>Zr</td>
<td>89.9047044</td>
<td>51.45</td>
</tr>
<tr>
<td>91</td>
<td>Zr</td>
<td>90.9056458</td>
<td>11.22</td>
</tr>
<tr>
<td>92</td>
<td>Zr</td>
<td>91.9050408</td>
<td>17.15</td>
</tr>
<tr>
<td>94</td>
<td>Zr</td>
<td>93.9063152</td>
<td>17.38</td>
</tr>
<tr>
<td>96</td>
<td>Zr</td>
<td>95.9082734</td>
<td>2.80</td>
</tr>
<tr>
<td>93</td>
<td>Nb</td>
<td>92.9063781</td>
<td>100.00</td>
</tr>
<tr>
<td>92</td>
<td>Mo</td>
<td>91.906811</td>
<td>14.77</td>
</tr>
<tr>
<td>94</td>
<td>Mo</td>
<td>93.9050883</td>
<td>9.23</td>
</tr>
<tr>
<td>95</td>
<td>Mo</td>
<td>94.9058421</td>
<td>15.90</td>
</tr>
<tr>
<td>96</td>
<td>Mo</td>
<td>95.9046795</td>
<td>16.68</td>
</tr>
<tr>
<td>97</td>
<td>Mo</td>
<td>96.9060215</td>
<td>9.56</td>
</tr>
<tr>
<td>98</td>
<td>Mo</td>
<td>97.9054082</td>
<td>24.19</td>
</tr>
<tr>
<td>100</td>
<td>Mo</td>
<td>99.907477</td>
<td>9.67</td>
</tr>
<tr>
<td>96</td>
<td>Ru</td>
<td>95.907598</td>
<td>5.54</td>
</tr>
<tr>
<td>98</td>
<td>Ru</td>
<td>97.905287</td>
<td>1.87</td>
</tr>
<tr>
<td>99</td>
<td>Ru</td>
<td>98.9059393</td>
<td>12.76</td>
</tr>
<tr>
<td>100</td>
<td>Ru</td>
<td>99.9042195</td>
<td>12.60</td>
</tr>
<tr>
<td>101</td>
<td>Ru</td>
<td>100.9055821</td>
<td>17.06</td>
</tr>
<tr>
<td>102</td>
<td>Ru</td>
<td>101.9043493</td>
<td>31.55</td>
</tr>
<tr>
<td>104</td>
<td>Ru</td>
<td>103.905433</td>
<td>18.62</td>
</tr>
<tr>
<td>103</td>
<td>Ru</td>
<td>102.905504</td>
<td>100.00</td>
</tr>
<tr>
<td>102</td>
<td>Pd</td>
<td>101.905609</td>
<td>1.02</td>
</tr>
<tr>
<td>104</td>
<td>Pd</td>
<td>103.904036</td>
<td>11.14</td>
</tr>
<tr>
<td>105</td>
<td>Pd</td>
<td>104.905085</td>
<td>22.33</td>
</tr>
<tr>
<td>106</td>
<td>Pd</td>
<td>105.903486</td>
<td>27.33</td>
</tr>
<tr>
<td>108</td>
<td>Pd</td>
<td>107.903892</td>
<td>26.46</td>
</tr>
<tr>
<td>110</td>
<td>Pd</td>
<td>109.905153</td>
<td>11.72</td>
</tr>
<tr>
<td>107</td>
<td>Ag</td>
<td>106.905097</td>
<td>51.839</td>
</tr>
<tr>
<td>109</td>
<td>Ag</td>
<td>108.904752</td>
<td>48.161</td>
</tr>
<tr>
<td>106</td>
<td>Cd</td>
<td>105.906459</td>
<td>1.25</td>
</tr>
<tr>
<td>108</td>
<td>Cd</td>
<td>107.904184</td>
<td>0.89</td>
</tr>
<tr>
<td>110</td>
<td>Cd</td>
<td>109.9030021</td>
<td>12.49</td>
</tr>
<tr>
<td>111</td>
<td>Cd</td>
<td>110.9041781</td>
<td>12.80</td>
</tr>
<tr>
<td>112</td>
<td>Cd</td>
<td>111.9027578</td>
<td>24.13</td>
</tr>
<tr>
<td>113</td>
<td>Cd</td>
<td>112.9044017</td>
<td>12.22</td>
</tr>
<tr>
<td>114</td>
<td>Cd</td>
<td>113.9033585</td>
<td>28.73</td>
</tr>
<tr>
<td>116</td>
<td>Cd</td>
<td>114.904756</td>
<td>7.49</td>
</tr>
<tr>
<td>113</td>
<td>In</td>
<td>112.904058</td>
<td>4.29</td>
</tr>
<tr>
<td>115</td>
<td>In</td>
<td>114.903878</td>
<td>95.71</td>
</tr>
<tr>
<td>112</td>
<td>Sn</td>
<td>111.904818</td>
<td>0.97</td>
</tr>
<tr>
<td>114</td>
<td>Sn</td>
<td>113.902779</td>
<td>0.66</td>
</tr>
<tr>
<td>115</td>
<td>Sn</td>
<td>114.903342</td>
<td>0.34</td>
</tr>
<tr>
<td>116</td>
<td>Sn</td>
<td>114.901741</td>
<td>14.54</td>
</tr>
<tr>
<td>117</td>
<td>Sn</td>
<td>116.902952</td>
<td>7.68</td>
</tr>
<tr>
<td>118</td>
<td>Sn</td>
<td>117.901603</td>
<td>24.22</td>
</tr>
<tr>
<td>119</td>
<td>Sn</td>
<td>118.903308</td>
<td>8.59</td>
</tr>
<tr>
<td>120</td>
<td>Sn</td>
<td>119.9021947</td>
<td>32.58</td>
</tr>
<tr>
<td>122</td>
<td>Sn</td>
<td>121.9034390</td>
<td>4.63</td>
</tr>
<tr>
<td>124</td>
<td>Sn</td>
<td>123.9052739</td>
<td>5.79</td>
</tr>
<tr>
<td>121</td>
<td>Sb</td>
<td>120.9038157</td>
<td>57.21</td>
</tr>
<tr>
<td>123</td>
<td>Sb</td>
<td>122.9042140</td>
<td>42.79</td>
</tr>
<tr>
<td>120</td>
<td>Te</td>
<td>119.904020</td>
<td>0.09</td>
</tr>
<tr>
<td>122</td>
<td>Te</td>
<td>121.9030439</td>
<td>2.55</td>
</tr>
<tr>
<td>123</td>
<td>Te</td>
<td>122.9042700</td>
<td>0.89</td>
</tr>
<tr>
<td>124</td>
<td>Te</td>
<td>123.9028179</td>
<td>4.74</td>
</tr>
<tr>
<td>125</td>
<td>Te</td>
<td>124.9044307</td>
<td>7.07</td>
</tr>
<tr>
<td>126</td>
<td>Te</td>
<td>125.9033117</td>
<td>18.84</td>
</tr>
<tr>
<td>128</td>
<td>Te</td>
<td>127.9044631</td>
<td>31.74</td>
</tr>
<tr>
<td>130</td>
<td>Te</td>
<td>129.9062244</td>
<td>34.08</td>
</tr>
<tr>
<td>127</td>
<td>I</td>
<td>126.904473</td>
<td>100.00</td>
</tr>
<tr>
<td>124</td>
<td>Xe</td>
<td>123.9058930</td>
<td>0.0952</td>
</tr>
<tr>
<td>126</td>
<td>Xe</td>
<td>125.904274</td>
<td>0.0890</td>
</tr>
<tr>
<td>128</td>
<td>Xe</td>
<td>127.9035313</td>
<td>1.9102</td>
</tr>
<tr>
<td>129</td>
<td>Xe</td>
<td>128.9047794</td>
<td>26.4006</td>
</tr>
<tr>
<td>130</td>
<td>Xe</td>
<td>129.9035080</td>
<td>4.0710</td>
</tr>
<tr>
<td>131</td>
<td>Xe</td>
<td>130.9050824</td>
<td>21.2324</td>
</tr>
<tr>
<td>132</td>
<td>Xe</td>
<td>131.9041535</td>
<td>26.9086</td>
</tr>
<tr>
<td>134</td>
<td>Xe</td>
<td>133.9053945</td>
<td>10.4357</td>
</tr>
<tr>
<td>136</td>
<td>Xe</td>
<td>135.907219</td>
<td>8.8573</td>
</tr>
<tr>
<td>133</td>
<td>Cs</td>
<td>132.905451933</td>
<td>100.00</td>
</tr>
<tr>
<td>130</td>
<td>Ba</td>
<td>129.9063208</td>
<td>0.106</td>
</tr>
<tr>
<td>132</td>
<td>Ba</td>
<td>131.9050613</td>
<td>0.101</td>
</tr>
<tr>
<td>134</td>
<td>Ba</td>
<td>133.904508</td>
<td>2.417</td>
</tr>
<tr>
<td>135</td>
<td>Ba</td>
<td>134.9056886</td>
<td>6.592</td>
</tr>
<tr>
<td>136</td>
<td>Ba</td>
<td>135.9045759</td>
<td>7.854</td>
</tr>
<tr>
<td>137</td>
<td>Ba</td>
<td>136.9058274</td>
<td>11.232</td>
</tr>
<tr>
<td>138</td>
<td>Ba</td>
<td>137.9052472</td>
<td>71.698</td>
</tr>
<tr>
<td>138</td>
<td>La</td>
<td>137.907172</td>
<td>0.090</td>
</tr>
<tr>
<td>139</td>
<td>La</td>
<td>138.9063533</td>
<td>99.910</td>
</tr>
<tr>
<td>136</td>
<td>Ce</td>
<td>135.907172</td>
<td>0.185</td>
</tr>
<tr>
<td>138</td>
<td>Ce</td>
<td>137.905991</td>
<td>0.251</td>
</tr>
<tr>
<td>140</td>
<td>Ce</td>
<td>139.9054387</td>
<td>88.450</td>
</tr>
<tr>
<td>142</td>
<td>Ce</td>
<td>141.909244</td>
<td>11.114</td>
</tr>
<tr>
<td>141</td>
<td>Pr</td>
<td>140.9076528</td>
<td>100.00</td>
</tr>
<tr>
<td>142</td>
<td>Nd</td>
<td>141.9077233</td>
<td>27.2</td>
</tr>
<tr>
<td>143</td>
<td>Nd</td>
<td>142.9098143</td>
<td>12.2</td>
</tr>
<tr>
<td>144</td>
<td>Nd</td>
<td>143.9100873</td>
<td>23.8</td>
</tr>
<tr>
<td>145</td>
<td>Nd</td>
<td>144.9125736</td>
<td>8.3</td>
</tr>
<tr>
<td>146</td>
<td>Nd</td>
<td>145.9131169</td>
<td>17.2</td>
</tr>
<tr>
<td>148</td>
<td>Nd</td>
<td>147.916893</td>
<td>5.7</td>
</tr>
<tr>
<td>150</td>
<td>Nd</td>
<td>149.920891</td>
<td>5.6</td>
</tr>
<tr>
<td>144</td>
<td>Sm</td>
<td>143.911999</td>
<td>3.07</td>
</tr>
<tr>
<td>147</td>
<td>Sm</td>
<td>146.9148979</td>
<td>14.99</td>
</tr>
<tr>
<td>148</td>
<td>Sm</td>
<td>147.9148227</td>
<td>11.24</td>
</tr>
<tr>
<td>149</td>
<td>Sm</td>
<td>148.9171847</td>
<td>13.82</td>
</tr>
<tr>
<td>150</td>
<td>Sm</td>
<td>149.9172755</td>
<td>7.38</td>
</tr>
<tr>
<td>152</td>
<td>Sm</td>
<td>151.9197324</td>
<td>26.75</td>
</tr>
<tr>
<td>154</td>
<td>Sm</td>
<td>153.9222093</td>
<td>22.75</td>
</tr>
<tr>
<td>151</td>
<td>Eu</td>
<td>150.9198502</td>
<td>47.81</td>
</tr>
<tr>
<td>153</td>
<td>Eu</td>
<td>152.9212303</td>
<td>52.19</td>
</tr>
<tr>
<td>152</td>
<td>Gd</td>
<td>151.9197910</td>
<td>0.20</td>
</tr>
<tr>
<td>154</td>
<td>Gd</td>
<td>153.9208656</td>
<td>2.18</td>
</tr>
<tr>
<td>155</td>
<td>Gd</td>
<td>154.9226220</td>
<td>14.80</td>
</tr>
<tr>
<td>156</td>
<td>Gd</td>
<td>155.9221227</td>
<td>20.47</td>
</tr>
<tr>
<td>157</td>
<td>Gd</td>
<td>156.9239601</td>
<td>15.65</td>
</tr>
<tr>
<td>158</td>
<td>Gd</td>
<td>157.924039</td>
<td>24.84</td>
</tr>
<tr>
<td>160</td>
<td>Gd</td>
<td>159.9270541</td>
<td>21.86</td>
</tr>
<tr>
<td>159</td>
<td>Tb</td>
<td>158.9253468</td>
<td>100.00</td>
</tr>
<tr>
<td>156</td>
<td>Dy</td>
<td>155.924283</td>
<td>0.056</td>
</tr>
<tr>
<td>158</td>
<td>Dy</td>
<td>157.924409</td>
<td>0.095</td>
</tr>
<tr>
<td>160</td>
<td>Dy</td>
<td>159.9251975</td>
<td>2.329</td>
</tr>
<tr>
<td>161</td>
<td>Dy</td>
<td>160.9269334</td>
<td>18.889</td>
</tr>
<tr>
<td>162</td>
<td>Dy</td>
<td>161.9267984</td>
<td>25.475</td>
</tr>
<tr>
<td>163</td>
<td>Dy</td>
<td>162.9287312</td>
<td>24.896</td>
</tr>
<tr>
<td>164</td>
<td>Dy</td>
<td>163.9291748</td>
<td>28.260</td>
</tr>
<tr>
<td>165</td>
<td>Ho</td>
<td>164.9303221</td>
<td>100.00</td>
</tr>
<tr>
<td>162</td>
<td>Er</td>
<td>161.928778</td>
<td>0.139</td>
</tr>
<tr>
<td>164</td>
<td>Er</td>
<td>163.929200</td>
<td>1.601</td>
</tr>
<tr>
<td>166</td>
<td>Er</td>
<td>165.9302931</td>
<td>33.503</td>
</tr>
<tr>
<td>167</td>
<td>Er</td>
<td>166.9320482</td>
<td>22.869</td>
</tr>
<tr>
<td>168</td>
<td>Er</td>
<td>167.9323702</td>
<td>26.978</td>
</tr>
<tr>
<td>170</td>
<td>Er</td>
<td>169.9354643</td>
<td>14.910</td>
</tr>
<tr>
<td>169</td>
<td>Tm</td>
<td>168.9342133</td>
<td>100.00</td>
</tr>
<tr>
<td>168</td>
<td>Yb</td>
<td>167.933897</td>
<td>0.13</td>
</tr>
<tr>
<td>170</td>
<td>Yb</td>
<td>169.9347618</td>
<td>3.04</td>
</tr>
<tr>
<td>171</td>
<td>Yb</td>
<td>170.9363258</td>
<td>14.28</td>
</tr>
<tr>
<td>172</td>
<td>Yb</td>
<td>171.9363815</td>
<td>21.83</td>
</tr>
<tr>
<td>173</td>
<td>Yb</td>
<td>172.9382108</td>
<td>16.13</td>
</tr>
<tr>
<td>174</td>
<td>Yb</td>
<td>173.9388621</td>
<td>31.83</td>
</tr>
<tr>
<td>176</td>
<td>Yb</td>
<td>175.9425717</td>
<td>12.76</td>
</tr>
<tr>
<td>175</td>
<td>Lu</td>
<td>174.9407718</td>
<td>97.41</td>
</tr>
<tr>
<td>176</td>
<td>Lu</td>
<td>175.9426863</td>
<td>2.59</td>
</tr>
<tr>
<td>174</td>
<td>Hf</td>
<td>173.940046</td>
<td>0.16</td>
</tr>
<tr>
<td>176</td>
<td>Hf</td>
<td>175.9414086</td>
<td>5.26</td>
</tr>
<tr>
<td>177</td>
<td>Hf</td>
<td>176.9432207</td>
<td>18.60</td>
</tr>
<tr>
<td>178</td>
<td>Hf</td>
<td>177.9436988</td>
<td>27.28</td>
</tr>
<tr>
<td>179</td>
<td>Hf</td>
<td>178.9458161</td>
<td>13.62</td>
</tr>
<tr>
<td>180</td>
<td>Hf</td>
<td>179.9465500</td>
<td>35.08</td>
</tr>
<tr>
<td>180</td>
<td>Ta</td>
<td>179.9474648</td>
<td>0.012</td>
</tr>
<tr>
<td>181</td>
<td>Ta</td>
<td>180.9479958</td>
<td>99.988</td>
</tr>
<tr>
<td>180</td>
<td>W</td>
<td>179.946704</td>
<td>0.12</td>
</tr>
<tr>
<td>182</td>
<td>W</td>
<td>181.9482042</td>
<td>26.50</td>
</tr>
<tr>
<td>183</td>
<td>W</td>
<td>182.9502230</td>
<td>14.31</td>
</tr>
<tr>
<td>184</td>
<td>W</td>
<td>183.950931</td>
<td>30.64</td>
</tr>
<tr>
<td>186</td>
<td>W</td>
<td>185.9543641</td>
<td>28.43</td>
</tr>
<tr>
<td>185</td>
<td>Re</td>
<td>184.9529550</td>
<td>37.40</td>
</tr>
<tr>
<td>187</td>
<td>Re</td>
<td>186.9557531</td>
<td>62.60</td>
</tr>
<tr>
<td>184</td>
<td>Os</td>
<td>183.9524891</td>
<td>0.02</td>
</tr>
<tr>
<td>186</td>
<td>Os</td>
<td>185.9538382</td>
<td>1.59</td>
</tr>
<tr>
<td>187</td>
<td>Os</td>
<td>186.9557505</td>
<td>1.96</td>
</tr>
<tr>
<td>188</td>
<td>Os</td>
<td>187.9558382</td>
<td>13.24</td>
</tr>
<tr>
<td>189</td>
<td>Os</td>
<td>188.9581475</td>
<td>16.15</td>
</tr>
<tr>
<td>190</td>
<td>Os</td>
<td>189.9584470</td>
<td>26.26</td>
</tr>
<tr>
<td>192</td>
<td>Os</td>
<td>191.9614807</td>
<td>40.78</td>
</tr>
<tr>
<td>191</td>
<td>Ir</td>
<td>190.9605940</td>
<td>37.3</td>
</tr>
<tr>
<td>193</td>
<td>Ir</td>
<td>192.9629264</td>
<td>62.7</td>
</tr>
<tr>
<td>190</td>
<td>Pt</td>
<td>189.959932</td>
<td>0.014</td>
</tr>
<tr>
<td>192</td>
<td>Pt</td>
<td>191.9610380</td>
<td>0.782</td>
</tr>
<tr>
<td>194</td>
<td>Pt</td>
<td>193.9626803</td>
<td>32.967</td>
</tr>
<tr>
<td>195</td>
<td>Pt</td>
<td>194.9647911</td>
<td>33.832</td>
</tr>
<tr>
<td>196</td>
<td>Pt</td>
<td>195.9649515</td>
<td>25.242</td>
</tr>
<tr>
<td>198</td>
<td>Pt</td>
<td>197.967893</td>
<td>7.163</td>
</tr>
<tr>
<td>197</td>
<td>Au</td>
<td>196.9665687</td>
<td>100.00</td>
</tr>
<tr>
<td>196</td>
<td>Hg</td>
<td>195.965833</td>
<td>0.15</td>
</tr>
<tr>
<td>198</td>
<td>Hg</td>
<td>197.966769</td>
<td>9.97</td>
</tr>
<tr>
<td>199</td>
<td>Hg</td>
<td>198.9682799</td>
<td>16.87</td>
</tr>
<tr>
<td>200</td>
<td>Hg</td>
<td>199.968326</td>
<td>23.10</td>
</tr>
<tr>
<td>201</td>
<td>Hg</td>
<td>200.9703023</td>
<td>13.18</td>
</tr>
<tr>
<td>202</td>
<td>Hg</td>
<td>201.9706430</td>
<td>29.86</td>
</tr>
<tr>
<td>204</td>
<td>Hg</td>
<td>203.9734939</td>
<td>6.78</td>
</tr>
<tr>
<td>203</td>
<td>Tl</td>
<td>202.9723442</td>
<td>29.52</td>
</tr>
<tr>
<td>205</td>
<td>Tl</td>
<td>204.9744275</td>
<td>70.48</td>
</tr>
<tr>
<td>204</td>
<td>Pb</td>
<td>203.9730436</td>
<td>1.4</td>
</tr>
<tr>
<td>206</td>
<td>Pb</td>
<td>205.974653</td>
<td>24.1</td>
</tr>
<tr>
<td>207</td>
<td>Pb</td>
<td>206.9758969</td>
<td>22.1</td>
</tr>
<tr>
<td>208</td>
<td>Pb</td>
<td>207.9766521</td>
<td>52.4</td>
</tr>
<tr>
<td>209</td>
<td>Bi</td>
<td>208.9803987</td>
<td>100.00</td>
</tr>
<tr>
<td>232</td>
<td>Th</td>
<td>232.0380553</td>
<td>100.00</td>
</tr>
<tr>
<td>231</td>
<td>Pa</td>
<td>231.0358840</td>
<td>100.00</td>
</tr>
<tr>
<td>234</td>
<td>U</td>
<td>234.0409521</td>
<td>0.0054</td>
</tr>
<tr>
<td>235</td>
<td>U</td>
<td>235.0439299</td>
<td>0.7204</td>
</tr>
<tr>
<td>238</td>
<td>U</td>
<td>238.0507882</td>
<td>99.2742</td>
</tr>"""

class Element:
    """Each element is an object"""
    def __init__(self, symbol):
        self.symbol = symbol
        self.isotopes = []

    def add_isotope(self, isotope, mass, abundance):
        self.isotopes.append([isotope, mass, abundance])


def process_raw(r):
    raw1 = raw_tabled.replace('\n','')
    raw2 = raw1.replace('<tr>','')
    raw3 = raw2.replace('<td>','')
    raw4 = raw3.split('</tr>')
    items = list ()
    for r in raw4:
        items.append(r.split('</td>'))
    elements = dict()
    
    items.remove([''])
    
    for i in items:
        if i[1] not in elements:
            elements[i[1]] = Element(i[1])
        elements[i[1]].add_isotope(int(i[0]), float(i[2]), float(i[3]))

    return elements


TABLE_OF_MASS = process_raw(raw_tabled)
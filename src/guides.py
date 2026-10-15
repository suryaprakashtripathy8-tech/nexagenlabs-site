"""Pillar guides. Each body is HTML; h2 ids feed the table of contents."""

BM = "https://benchmate.nexagenlabs.com"

GUIDES = [
# ---------------------------------------------------------------- 1
{
"slug": "how-to-calculate-molarity",
"title": "How to Calculate Molarity: Formula, Worked Examples and Common Mistakes",
"short": "How to calculate molarity",
"description": "Molarity formula explained for the bench: mass = M × V × MW, worked examples for NaCl, Tris and EDTA, hydrate traps and a free molarity calculator.",
"tool": ("Molarity & Dilution calculator", BM + "/molarity"),
"minutes": 7, "date": "2026-10-15",
"keywords": "molarity calculation, molarity formula, how to make a 1 M solution, grams to molarity",
"toc": [("what","What molarity means"),("formula","The one formula you need"),("examples","Worked examples"),("hydrates","Hydrates, purity and the wrong MW"),("mistakes","Mistakes that cost a week")],
"body": """
<p>Molarity is the first number most people get wrong in a new lab. Not because the maths is hard. It is because the bottle on the shelf rarely matches the number in the protocol.</p>
<h2 id="what">What molarity means</h2>
<p>Molarity (M) is moles of solute per litre of final solution. A 1 M NaCl solution holds 1 mole of NaCl, which is 58.44 g, in every litre of liquid once the volume is made up. The key words are <strong>final solution</strong>. You do not add 58.44 g of salt to 1 L of water. You dissolve it in less water and then bring the volume up to 1 L.</p>
<p>The smaller units scale by a thousand each time: 1 M = 1000 mM = 1,000,000 µM. Most working solutions in molecular biology sit in the mM and µM range. Stocks usually sit at 0.5 M to 5 M.</p>
<h2 id="formula">The one formula you need</h2>
<div class="formula">mass (g) = molarity (mol/L) × volume (L) × molecular weight (g/mol)</div>
<p>Everything else is a rearrangement. If you have the mass and want the molarity, divide by volume and MW. If you have a target molarity and a fixed mass, solve for volume. Keep the units in litres and mol/L while you calculate, and convert to mL or mM only at the end. Most slips happen in the unit change, not in the multiplication.</p>
<h2 id="examples">Worked examples</h2>
<h3>500 mL of 1 M NaCl</h3>
<p>1 mol/L × 0.5 L × 58.44 g/mol = <strong>29.22 g</strong>. Dissolve in about 400 mL of water, then make up to 500 mL.</p>
<h3>250 mL of 1 M Tris base</h3>
<p>Tris base has an MW of 121.14 g/mol. 1 × 0.25 × 121.14 = <strong>30.29 g</strong>. Dissolve, adjust pH with HCl, and only then make up to volume, because acid addition changes the volume.</p>
<h3>100 mL of 0.5 M EDTA, pH 8.0</h3>
<p>Most labs buy disodium EDTA dihydrate (MW 372.24 g/mol). 0.5 × 0.1 × 372.24 = <strong>18.61 g</strong>. It will not dissolve until the pH climbs towards 8.0, so add NaOH while stirring. People often think the powder is bad. It is just the pH.</p>
<table><thead><tr><th>Target</th><th>Volume</th><th>MW (g/mol)</th><th>Weigh</th></tr></thead><tbody>
<tr><td>1 M NaCl</td><td>500 mL</td><td>58.44</td><td>29.22 g</td></tr>
<tr><td>1 M Tris base</td><td>250 mL</td><td>121.14</td><td>30.29 g</td></tr>
<tr><td>0.5 M Na₂EDTA·2H₂O</td><td>100 mL</td><td>372.24</td><td>18.61 g</td></tr>
<tr><td>1 M MgCl₂·6H₂O</td><td>100 mL</td><td>203.30</td><td>20.33 g</td></tr>
</tbody></table>
<h2 id="hydrates">Hydrates, purity and the wrong MW</h2>
<p>Read the label, not the protocol. MgCl₂ anhydrous is 95.21 g/mol and the hexahydrate is 203.30 g/mol. Use the wrong one and your stock is off by more than a factor of two. The same trap sits in CaCl₂, CuSO₄, sodium phosphates and EDTA salts.</p>
<p>For reagents with stated purity below about 98%, correct the mass: divide by the purity fraction. A 95% pure reagent needs 1/0.95, about 5% more mass, for the same molarity. For routine buffers this rarely matters. For standards and enzyme assays it does.</p>
<div class="callout tip"><p><strong>Bench habit:</strong> write the formula weight from the bottle on the tube label next to the molarity. Six months later, when a result looks odd, that one number tells you whether the stock was right.</p></div>
<h2 id="mistakes">Mistakes that cost a week</h2>
<ul>
<li><strong>Adding solute to the full final volume of water.</strong> The final volume ends up larger than planned, hence the concentration is lower.</li>
<li><strong>mL vs L.</strong> Typing 500 instead of 0.5 gives a 1000-fold error. Keep litres until the last step.</li>
<li><strong>Using the anhydrous MW for a hydrate.</strong> See above. Check every salt.</li>
<li><strong>pH-ing after making up to volume.</strong> Acid or base added later dilutes the solution a little and shifts the final concentration.</li>
<li><strong>Weighing hygroscopic salts slowly.</strong> CaCl₂ and MgCl₂ pull water from the air. Weigh fast and close the bottle.</li>
</ul>
<p>If you would rather not do this by hand at 7 pm, BenchMate's molarity tool runs the same formula with the MW pulled from a verified compound list, so the hydrate question is answered for you.</p>
""",
"faq": [
("What is the formula for molarity?","Molarity equals moles of solute divided by litres of final solution. To find how much to weigh, use mass (g) = molarity (mol/L) × volume (L) × molecular weight (g/mol)."),
("How do I make a 1 M solution?","Weigh the compound's molecular weight in grams for each litre you need, dissolve it in less than the final volume of water, then make up to the final volume. For 1 L of 1 M NaCl, weigh 58.44 g."),
("Does the hydrate form change the molarity calculation?","Yes. Use the molecular weight printed on your bottle, including water of hydration. MgCl₂·6H₂O is 203.30 g/mol while anhydrous MgCl₂ is 95.21 g/mol."),
("What is the difference between molarity and molality?","Molarity is moles per litre of solution. Molality is moles per kilogram of solvent. Bench protocols almost always use molarity."),
],
},
# ---------------------------------------------------------------- 2
{
"slug": "c1v1-c2v2-dilution-guide",
"title": "C1V1 = C2V2: The Dilution Equation With Worked Lab Examples",
"short": "C1V1 = C2V2 dilution guide",
"description": "How to use C1V1 = C2V2 for lab dilutions: step-by-step examples, unit traps, 10X to 1X buffers, and when the equation does not apply. Free dilution calculator.",
"tool": ("C1V1 dilution calculator", BM + "/molarity"),
"minutes": 6, "date": "2026-10-15",
"keywords": "c1v1 c2v2, dilution equation, dilution calculator, how to dilute a stock solution",
"toc": [("idea","The idea in one line"),("steps","Four steps, every time"),("examples","Worked examples"),("units","The unit trap"),("limits","When C1V1 does not work")],
"body": """
<p>C1V1 = C2V2 is the most used equation in any wet lab. It is also the one people stop thinking about, which is how a 10X buffer ends up at 0.1X.</p>
<h2 id="idea">The idea in one line</h2>
<p>When you dilute, the amount of solute does not change. Only the volume does. The amount before (C₁ × V₁) equals the amount after (C₂ × V₂).</p>
<div class="formula">C₁ × V₁ = C₂ × V₂ &nbsp;→&nbsp; V₁ = (C₂ × V₂) / C₁</div>
<p>C₁ is your stock concentration. V₁ is how much stock you take. C₂ is the concentration you want. V₂ is the final total volume. Three of these you know. The fourth you solve for, and nine times out of ten it is V₁.</p>
<h2 id="steps">Four steps, every time</h2>
<ol>
<li>Write down C₁, C₂ and V₂ with units.</li>
<li>Put C₁ and C₂ in the same unit. Put V₂ in the unit you want V₁ in.</li>
<li>Solve V₁ = (C₂ × V₂) / C₁.</li>
<li>Diluent volume = V₂ − V₁. Add stock to diluent, not the other way round, when the stock is an acid or a concentrated organic.</li>
</ol>
<h2 id="examples">Worked examples</h2>
<h3>10X TBE to 1 L of 1X</h3>
<p>V₁ = (1X × 1000 mL) / 10X = <strong>100 mL</strong> of 10X stock plus 900 mL water. The "X" works as a unit as long as both sides use it.</p>
<h3>1 M Tris to 50 mL of 50 mM</h3>
<p>Convert first: 50 mM = 0.05 M. V₁ = (0.05 × 50) / 1 = <strong>2.5 mL</strong> stock plus 47.5 mL diluent.</p>
<h3>10 mM drug stock to 200 µL of 25 µM</h3>
<p>10 mM = 10,000 µM. V₁ = (25 × 200) / 10,000 = <strong>0.5 µL</strong>. That is below what most pipettes deliver accurately. Do an intermediate dilution first, for example 1:10 to 1 mM, then take 5 µL of that into 195 µL.</p>
<div class="callout"><p><strong>Rule of thumb:</strong> if V₁ comes out under about 1 µL, or under 1% of a P20's range, do an intermediate dilution. The error in a 0.5 µL pipetting step can be larger than the effect you are measuring.</p></div>
<h2 id="units">The unit trap</h2>
<p>The equation does not care which units you use. It only cares that they match. Mixing mM on one side and µM on the other is the classic 1000-fold error. So is mg/mL against µg/µL. These last two are actually equal (1 mg/mL = 1 µg/µL), and people convert anyway and get it wrong.</p>
<table><thead><tr><th>Unit</th><th>Equals</th></tr></thead><tbody>
<tr><td>1 M</td><td>1000 mM = 10⁶ µM</td></tr>
<tr><td>1 mM</td><td>1000 µM = 10⁶ nM</td></tr>
<tr><td>1 mg/mL</td><td>1 µg/µL = 1 g/L</td></tr>
<tr><td>1 L</td><td>1000 mL = 10⁶ µL</td></tr>
</tbody></table>
<h2 id="limits">When C1V1 does not work</h2>
<ul>
<li><strong>Mixing two different solutions that both contain the solute.</strong> Add the amounts separately: C₁V₁ + C₂V₂ = C₃V₃.</li>
<li><strong>Solvents that change volume on mixing.</strong> Ethanol and water do not add linearly. 50 mL ethanol plus 50 mL water gives a bit less than 100 mL. For exact % v/v, make up to final volume.</li>
<li><strong>Percent w/w solutions</strong> such as concentrated HCl or ammonia. You need density to convert to molarity first.</li>
</ul>
<p>BenchMate solves C1V1 in either direction, handles the unit conversion, and warns you when V₁ is too small to pipette.</p>
""",
"faq": [
("What does C1V1 = C2V2 mean?","C₁ is the stock concentration, V₁ the volume of stock you take, C₂ the final concentration and V₂ the final volume. The amount of solute stays the same, so C₁V₁ equals C₂V₂."),
("How do I dilute 10X buffer to 1X?","Take one tenth of the final volume as 10X stock and make up the rest with water. For 1 L of 1X, use 100 mL of 10X and 900 mL of water."),
("Can I use different units for C1 and C2?","No. C₁ and C₂ must be in the same unit, and V₁ comes out in whatever unit you used for V₂."),
("What if the stock volume is too small to pipette?","Make an intermediate dilution first, for example 1:10 or 1:100, then dilute that to the final concentration."),
],
},
# ---------------------------------------------------------------- 3
{
"slug": "serial-dilution-guide",
"title": "Serial Dilutions Made Simple: Dilution Factors, Tables and Plating Math",
"short": "Serial dilution guide",
"description": "How to plan a serial dilution: dilution factor, 1:10 and 1:2 series tables, CFU back-calculation and pipetting errors that compound. Free serial dilution calculator.",
"tool": ("Serial dilution table", BM + "/molarity"),
"minutes": 6, "date": "2026-10-15",
"keywords": "serial dilution, dilution factor, serial dilution calculation, CFU calculation",
"toc": [("why","Why dilute in series"),("factor","Dilution factor"),("tables","Ready-made series"),("cfu","Back-calculating CFU/mL"),("errors","How errors compound")],
"body": """
<p>A serial dilution is a chain of small, identical dilutions. It gets you from a dense culture or a concentrated standard down to a countable or measurable range without ever pipetting a tiny volume.</p>
<h2 id="why">Why dilute in series</h2>
<p>Getting from 10⁹ cells/mL to 100 cells/mL in one step would need a 1:10,000,000 dilution. No pipette does that. Six 1:10 steps do it with 100 µL into 900 µL each time. Each step is easy to pipette and easy to check.</p>
<h2 id="factor">Dilution factor</h2>
<div class="formula">dilution factor = final volume / sample volume = (sample + diluent) / sample</div>
<p>100 µL into 900 µL is a 1:10 dilution, factor 10. 50 µL into 50 µL is 1:2. The total dilution after n identical steps is the step factor raised to n. Six 1:10 steps give 10⁶.</p>
<div class="callout tip"><p>"1:10" in most biology protocols means 1 part in 10 total, not 1 part plus 10 parts. A few older chemistry texts use the second meaning. If a protocol is ambiguous, check what total volume it expects.</p></div>
<h2 id="tables">Ready-made series</h2>
<h3>Tenfold series (100 µL into 900 µL)</h3>
<table><thead><tr><th>Tube</th><th>Dilution</th><th>From 10 mM stock</th></tr></thead><tbody>
<tr><td>1</td><td>10⁻¹</td><td>1 mM</td></tr>
<tr><td>2</td><td>10⁻²</td><td>100 µM</td></tr>
<tr><td>3</td><td>10⁻³</td><td>10 µM</td></tr>
<tr><td>4</td><td>10⁻⁴</td><td>1 µM</td></tr>
<tr><td>5</td><td>10⁻⁵</td><td>100 nM</td></tr>
</tbody></table>
<h3>Twofold series (for IC₅₀ and MIC plates)</h3>
<p>Put 100 µL diluent in each well, add 100 µL of the top concentration to well 1, mix, and carry 100 µL across. Discard 100 µL from the last well so every well ends at the same volume. Eight wells span a 128-fold range. Twelve wells span 2048-fold.</p>
<h2 id="cfu">Back-calculating CFU/mL</h2>
<div class="formula">CFU/mL = colonies ÷ (volume plated in mL × dilution)</div>
<p>Say 10⁻⁶ gives 54 colonies from 100 µL plated. CFU/mL = 54 / (0.1 × 10⁻⁶) = <strong>5.4 × 10⁸ CFU/mL</strong>. Count plates in the 30-300 colony range. Below that the count is noisy. Above it colonies merge.</p>
<h2 id="errors">How errors compound</h2>
<p>Each step carries its own pipetting error, and the errors multiply down the chain. A 2% error per step becomes about 13% after six steps (1.02⁶ ≈ 1.13). Three habits keep it down:</p>
<ul>
<li><strong>Change tips every step.</strong> Carry-over from a dense tube inflates every tube after it.</li>
<li><strong>Mix properly.</strong> Pipette up and down 5-8 times or vortex briefly. Unmixed tubes are the biggest source of bad series.</li>
<li><strong>Pre-wet the tip</strong> for viscous or protein-rich samples.</li>
</ul>
<p>BenchMate builds a serial dilution table for any start concentration, step factor and number of tubes, and prints it as a bench sheet.</p>
""",
"faq": [
("How do you calculate a dilution factor?","Divide the final volume by the sample volume. 100 µL of sample in 900 µL of diluent gives 1000 µL total, a dilution factor of 10."),
("How do I calculate the total dilution of a serial dilution?","Multiply the dilution factors of each step. Six 1:10 steps give a total dilution of 10⁶."),
("How do I calculate CFU/mL from a plate count?","Divide the colony count by the volume plated in mL times the dilution. 54 colonies from 0.1 mL of a 10⁻⁶ dilution gives 5.4 × 10⁸ CFU/mL."),
("Which plates should I count?","Plates with roughly 30 to 300 colonies give the most reliable counts."),
],
},
# ---------------------------------------------------------------- 4
{
"slug": "how-to-prepare-buffers",
"title": "How to Prepare Lab Buffers: PBS and Tris-HCl Recipes That Work",
"short": "How to prepare lab buffers",
"description": "Step-by-step buffer preparation: choosing a buffer by pKa, 1X PBS and 1 M Tris-HCl recipes, temperature effects on Tris pH, and pH meter habits. Free buffer recipe generator.",
"tool": ("Buffer Recipe Generator", BM + "/buffer"),
"minutes": 8, "date": "2026-10-15",
"keywords": "how to make PBS, Tris-HCl buffer preparation, buffer recipe, buffer pKa table",
"toc": [("choose","Choose by pKa"),("pbs","1X PBS, pH 7.4"),("tris","1 M Tris-HCl"),("temp","Temperature changes Tris pH"),("meter","pH meter habits")],
"body": """
<p>A buffer only works close to its pKa. Most buffer problems start with ignoring that, or with a pH meter that nobody calibrated this week.</p>
<h2 id="choose">Choose by pKa</h2>
<p>A buffer resists pH change best within about one unit of its pKa. Outside that range it is just salt water with a pH number on the label.</p>
<table><thead><tr><th>Buffer</th><th>pKa (25 °C)</th><th>Useful range</th></tr></thead><tbody>
<tr><td>Acetate</td><td>4.76</td><td>3.8-5.8</td></tr>
<tr><td>MES</td><td>6.1</td><td>5.5-6.7</td></tr>
<tr><td>Phosphate (H₂PO₄⁻)</td><td>7.2</td><td>6.2-8.2</td></tr>
<tr><td>HEPES</td><td>7.5</td><td>6.8-8.2</td></tr>
<tr><td>Tris</td><td>8.1</td><td>7.0-9.0</td></tr>
<tr><td>Glycine (amine)</td><td>9.6</td><td>8.8-10.6</td></tr>
</tbody></table>
<p>Then check compatibility. Phosphate precipitates with calcium and inhibits some kinases. Tris has a primary amine, so it reacts with NHS esters and aldehydes. HEPES can make peroxide under light in some media. The right buffer is the one your downstream step tolerates.</p>
<h2 id="pbs">1X PBS, pH 7.4 (1 L)</h2>
<table><thead><tr><th>Component</th><th>Amount</th><th>Final</th></tr></thead><tbody>
<tr><td>NaCl</td><td>8.0 g</td><td>137 mM</td></tr>
<tr><td>KCl</td><td>0.2 g</td><td>2.7 mM</td></tr>
<tr><td>Na₂HPO₄ (anhydrous)</td><td>1.44 g</td><td>10 mM</td></tr>
<tr><td>KH₂PO₄</td><td>0.24 g</td><td>1.8 mM</td></tr>
</tbody></table>
<ol>
<li>Dissolve in about 800 mL of purified water.</li>
<li>Check pH. It usually lands near 7.4. Adjust with HCl or NaOH only if needed.</li>
<li>Make up to 1 L. Autoclave or filter (0.22 µm) for cell work.</li>
</ol>
<p>If your Na₂HPO₄ is the heptahydrate or dodecahydrate, the mass changes. Heptahydrate: 2.72 g. Dodecahydrate: 3.63 g. Check the bottle.</p>
<h2 id="tris">1 M Tris-HCl (100 mL)</h2>
<ol>
<li>Dissolve 12.11 g Tris base in about 70 mL water.</li>
<li>Bring to the temperature you will use the buffer at.</li>
<li>Add concentrated HCl slowly with stirring. Roughly 4.2 mL takes it to pH 8.0, about 6 mL to pH 7.6 and about 7 mL to pH 7.4 at room temperature. Treat these as starting points and trust the meter.</li>
<li>Make up to 100 mL.</li>
</ol>
<h2 id="temp">Temperature changes Tris pH</h2>
<p>Tris pH drops about 0.028 units for every 1 °C rise. A buffer set to pH 8.0 at 25 °C reads about 8.6 at 4 °C and about 7.7 at 37 °C. That is not a small error for an enzyme with a narrow pH optimum. Set Tris at the temperature of use, or correct for it. Phosphate and HEPES shift much less.</p>
<div class="callout"><p><strong>Do not use a standard pH electrode in Tris without checking.</strong> Some silver/silver chloride reference junctions react with Tris and drift. Use a Tris-compatible electrode or a double-junction probe if you make Tris buffers daily.</p></div>
<h2 id="meter">pH meter habits</h2>
<ul>
<li>Calibrate with two buffers that bracket your target, every day you use the meter.</li>
<li>Stir gently and wait for a stable reading. Rushing is the common error.</li>
<li>Approach the target slowly. Overshoot and back-titration add salt you did not plan for.</li>
<li>Rinse the probe between solutions and store it wet in storage solution, never in water.</li>
</ul>
<p>BenchMate's buffer generator scales 40 common recipes to any volume and pH, and flags the temperature effect for Tris.</p>
""",
"faq": [
("How do I make 1X PBS?","For 1 L: dissolve 8.0 g NaCl, 0.2 g KCl, 1.44 g Na₂HPO₄ and 0.24 g KH₂PO₄ in about 800 mL water, check the pH is 7.4, then make up to 1 L and sterilise."),
("Why does my Tris buffer pH change in the cold room?","Tris pH falls about 0.028 units per °C rise, so it reads higher when cold. Set the pH at the temperature you will use the buffer."),
("How do I choose a buffer?","Pick a buffer with a pKa within about one unit of your target pH, then check it does not interfere with your enzymes, metals or chemistry."),
("Should I adjust pH before or after making up to volume?","Adjust pH before the final volume adjustment, because the acid or base you add takes up volume."),
],
},
# ---------------------------------------------------------------- 5
{
"slug": "percent-solutions-w-v-v-v",
"title": "Percent Solutions Explained: w/v, v/v and w/w With Lab Examples",
"short": "Percent solutions: w/v, v/v, w/w",
"description": "What % w/v, % v/v and % w/w mean, how to make 70% ethanol, 10% SDS and 1% agarose, and how to convert percent to molarity. Free percent-solution calculator.",
"tool": ("Percent-Solution Generator", BM + "/percent"),
"minutes": 6, "date": "2026-10-15",
"keywords": "percent solution, w/v percent, v/v percent, 70% ethanol preparation, percent to molarity",
"toc": [("types","Three kinds of percent"),("wv","% w/v in practice"),("vv","% v/v and 70% ethanol"),("ww","% w/w and concentrated reagents"),("convert","Percent to molarity")],
"body": """
<p>"Make a 10% solution" is not a complete instruction. Ten percent of what, by what? The answer changes the recipe.</p>
<h2 id="types">Three kinds of percent</h2>
<table><thead><tr><th>Type</th><th>Means</th><th>Typical use</th></tr></thead><tbody>
<tr><td>% w/v</td><td>grams per 100 mL of solution</td><td>SDS, agarose, glucose, NaCl</td></tr>
<tr><td>% v/v</td><td>mL per 100 mL of solution</td><td>ethanol, glycerol, Triton X-100</td></tr>
<tr><td>% w/w</td><td>grams per 100 g of solution</td><td>concentrated acids and bases</td></tr>
</tbody></table>
<p>When a protocol says % with a solid, assume w/v. With a liquid, assume v/v. When it is a commercial concentrated acid, it is w/w.</p>
<h2 id="wv">% w/v in practice</h2>
<div class="formula">grams needed = (% w/v ÷ 100) × final volume (mL)</div>
<ul>
<li><strong>10% SDS, 100 mL:</strong> 10 g SDS, dissolve in about 80 mL water, make up to 100 mL. Weigh it in a fume hood or with a mask. Do not autoclave SDS. Warm gently if it precipitates in the cold.</li>
<li><strong>1% agarose gel, 100 mL:</strong> 1 g agarose in 100 mL 1X TAE or TBE. Microwave until fully clear. Water evaporates while boiling, so top up with water to the starting weight if you care about exact percentage.</li>
<li><strong>0.9% NaCl (saline), 1 L:</strong> 9 g NaCl. That is about 154 mM.</li>
</ul>
<h2 id="vv">% v/v and 70% ethanol</h2>
<p>For 100 mL of 70% ethanol from absolute ethanol: 70 mL ethanol, then make up to 100 mL with water. Do not just add 30 mL water. Ethanol and water shrink when mixed, so 70 + 30 gives a bit under 100 mL and a slightly higher percentage.</p>
<p>From 95% ethanol, use C1V1: V₁ = (70 × 100) / 95 = <strong>73.7 mL</strong>, then make up to 100 mL.</p>
<div class="callout tip"><p>Glycerol is so viscous that pipetting it by volume is unreliable. Weigh it instead. Glycerol density is about 1.26 g/mL, so 50 mL is about 63 g.</p></div>
<h2 id="ww">% w/w and concentrated reagents</h2>
<p>Concentrated HCl is about 37% w/w with a density near 1.19 g/mL. To use it you need both numbers. That is why it gets its own row in the next section.</p>
<h2 id="convert">Percent to molarity</h2>
<div class="formula">M = (% w/v × 10) ÷ MW &nbsp;&nbsp;|&nbsp;&nbsp; M = (% w/w × density × 10) ÷ MW</div>
<ul>
<li>0.9% NaCl: (0.9 × 10) / 58.44 = 0.154 M.</li>
<li>37% HCl (density 1.19): (37 × 1.19 × 10) / 36.46 ≈ 12.1 M.</li>
<li>28-30% ammonia (density about 0.90): roughly 14.8 M at 28%. Check your bottle's assay.</li>
</ul>
<p>Always add concentrated acid to water, slowly, in a fume hood. Never water to acid.</p>
<p>BenchMate's percent tool gives the mass or volume for any %, converts to molarity, and warns about viscous and hazardous reagents.</p>
""",
"faq": [
("What does % w/v mean?","Grams of solute per 100 mL of final solution. A 10% w/v solution has 10 g in every 100 mL."),
("How do I make 70% ethanol?","Measure 70 mL of absolute ethanol and make up to 100 mL with water. From 95% ethanol, use 73.7 mL and make up to 100 mL."),
("How do I convert percent to molarity?","For % w/v, multiply the percent by 10 and divide by the molecular weight. For % w/w, also multiply by the density in g/mL."),
("What molarity is 37% HCl?","About 12.1 M, using a density of 1.19 g/mL and an MW of 36.46 g/mol."),
],
},
# ---------------------------------------------------------------- 6
{
"slug": "dna-concentration-ng-ul-to-nm",
"title": "DNA Concentration: Converting ng/µL to nM and Copy Number",
"short": "ng/µL to nM and copy number",
"description": "Convert DNA and RNA concentration from ng/µL to nM, pmol and copy number. A260 basics, purity ratios, primer and plasmid examples. Free nucleic acid unit converter.",
"tool": ("Unit Converter (ng/µL)", BM + "/converter"),
"minutes": 7, "date": "2026-10-15",
"keywords": "ng/ul to nM, DNA copy number calculation, A260 concentration, convert DNA concentration",
"toc": [("a260","From A260 to ng/µL"),("purity","Purity ratios"),("nm","ng/µL to nM"),("copies","Copy number"),("examples","Worked examples")],
"body": """
<p>Your spectrophotometer reports ng/µL. Ligation, library prep and qPCR standards want molar amounts or copies. The conversion depends on length, which is why the same 50 ng/µL means very different things for a primer and a plasmid.</p>
<h2 id="a260">From A260 to ng/µL</h2>
<p>At 260 nm, an absorbance of 1.0 (1 cm path) corresponds to about:</p>
<table><thead><tr><th>Nucleic acid</th><th>1 A260 unit</th></tr></thead><tbody>
<tr><td>dsDNA</td><td>50 ng/µL</td></tr>
<tr><td>ssDNA</td><td>33 ng/µL</td></tr>
<tr><td>RNA</td><td>40 ng/µL</td></tr>
</tbody></table>
<p>Short oligos are better quantified with their own extinction coefficient, which depends on sequence. The supplier's sheet gives it.</p>
<h2 id="purity">Purity ratios</h2>
<ul>
<li><strong>A260/A280:</strong> about 1.8 for clean DNA, about 2.0 for clean RNA. Low values suggest protein or phenol.</li>
<li><strong>A260/A230:</strong> usually 2.0-2.2. Low values point to guanidine salts, EDTA or carbohydrate carry-over.</li>
</ul>
<p>A good concentration with a bad A260/A230 can still fail a ligation. Fluorometric assays (dye-based) are more accurate for low concentrations and for libraries.</p>
<h2 id="nm">ng/µL to nM</h2>
<div class="formula">nM (dsDNA) = (ng/µL × 10⁶) ÷ (length in bp × 650)</div>
<p>650 g/mol is a common average mass for one base pair of dsDNA (some sources use 660, a 1.5% difference). For ssDNA use about 330 g/mol per base. For RNA use about 340 g/mol per base.</p>
<h2 id="copies">Copy number</h2>
<div class="formula">copies/µL = (ng/µL × 6.022 × 10²³) ÷ (length × 650 × 10⁹)</div>
<p>This is the number you need for qPCR standard curves and for checking whether a dilution series actually reaches single copies.</p>
<h2 id="examples">Worked examples</h2>
<table><thead><tr><th>Sample</th><th>Conc.</th><th>Length</th><th>nM</th><th>copies/µL</th></tr></thead><tbody>
<tr><td>PCR product</td><td>50 ng/µL</td><td>500 bp</td><td>153.8</td><td>9.3 × 10¹⁰</td></tr>
<tr><td>Plasmid</td><td>100 ng/µL</td><td>5000 bp</td><td>30.8</td><td>1.9 × 10¹⁰</td></tr>
<tr><td>Library</td><td>2 ng/µL</td><td>400 bp</td><td>7.7</td><td>4.6 × 10⁹</td></tr>
</tbody></table>
<p>For ligation, the usual vector:insert molar ratio is 1:3. With a 3 kb vector at 50 ng, a 1 kb insert needs about 50 ng (50 × 1/3 × 3 = 50 ng). Length does the work.</p>
<div class="callout tip"><p>For library pooling, convert every library to nM using its own average fragment length from the bioanalyzer trace, not a guessed length. A wrong length gives a wrong pool.</p></div>
<p>BenchMate converts between ng/µL, nM and copies for dsDNA, ssDNA and RNA in one step.</p>
""",
"faq": [
("How do I convert ng/µL to nM for DNA?","For dsDNA, multiply ng/µL by 10⁶ and divide by length in bp times 650. A 500 bp product at 50 ng/µL is about 154 nM."),
("How do I calculate DNA copy number?","Copies/µL = (ng/µL × 6.022 × 10²³) ÷ (length in bp × 650 × 10⁹)."),
("What is a good A260/A280 ratio?","About 1.8 for DNA and about 2.0 for RNA."),
("What does 1 A260 unit equal?","About 50 ng/µL for dsDNA, 33 ng/µL for ssDNA and 40 ng/µL for RNA with a 1 cm path."),
],
},
]

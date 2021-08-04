(function () {
    'use strict';
  
    function packageHierarchy(classes) {
      var map = {};
    
      function find(name, data) {
        var node = map[name], i;
        if (!node) {
          node = map[name] = data || {name: name, children: []};
          if (name.length) {
            node.parent = find(name.substring(0, i = name.lastIndexOf(".")));
            node.parent.children.push(node);
            node.key = name.substring(i + 1);
          }
        }
        return node;
      }
    
      classes.forEach(function(d) {
        find(d.name, d);
      });
    
      return d3.hierarchy(map[""]);
    }
  
    function packageImports(nodes) {
      var map = {},
          imports = [];
    
      // Compute a map from name to node.
      console.log(nodes)
      nodes.forEach(function(d) {
        map[d.data.name] = d;
      });
    
      // For each import, construct a link from the source to target node.
      nodes.forEach(function(d) {
        if (d.data.imports) d.data.imports.forEach(function(i) {
          imports.push(map[d.data.name].path(map[i]));
        });
  
      });
    
      return imports;
    }
 
    function render(data){
      const diameter = 1200
      const radius = diameter / 2
      const innerRadius = radius - 120;
      const k = 6
  
      var cluster = d3.cluster()
      .size([360, innerRadius]);
  
      var line = d3.lineRadial()
          .curve(d3.curveBundle.beta(0.85))
          .radius(function(d) { return d.y; })
          .angle(function(d) { return d.x / 180 * Math.PI; });
  
      var svg = d3.select("body").append("svg")
          .attr("width", diameter)
          .attr("height", diameter)
        .append("g")
          .attr("transform", "translate(" + radius + "," + radius + ")");
  
      const link = svg.append("g").selectAll(".link")
      const node = svg.append("g").selectAll(".node");
  
      const root = packageHierarchy(data)
        //.sum(function(d) { return d.size; });
      
      cluster(root);
  
  
      link.data(packageImports(root.leaves()))
        .enter().append("path")
          .each(function(d) { d.source = d[0], d.target = d[d.length - 1]; })
          .attr("class", "link")
          .attr("d", line)
          .attr("stroke", "black");
  
      node.data(root.leaves())
        .enter().append("text")
          .attr("class", "node")
          .attr("dy", "0.31em")
          .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
          .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
          .text(function(d) { return d.data.key; });
  
    }
  
    const url = "https://raw.githubusercontent.com/AndresRubianoM/exportVisualization/master/dataGraph.csv"
    d3.csv(url).then( data => {
        const correctData = []
        let imports = ""
        console.log(data)
        for (const row of data){
          imports = row.imports.replace("[", "").replace("]", "").replaceAll("'", "").replace(/\"+/g,"")
          imports = imports.split(", ")
          if (row.imports === ""){
            imports = []
          }
          row.name = row.name.replace(/\"+/g,"").replace("'", "")
          correctData.push({ name:row.name, imports:imports })
        }
        render(correctData)
    })
  }()) 
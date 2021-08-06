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
      let map = {};
      let imports = [];
    
      nodes.forEach(function(d) {
        map[d.data.name] = d;
      });
    
      nodes.forEach(function(d) {
        if (d.data.imports) {
          d.data.imports.forEach(function(i) {
            imports.push(map[d.data.name].path(map[i]));    
          })
        };
      });
      
      
      return imports;
    }

    function dataOrder(nodes, imports){
      nodes.forEach(d=>{
        d.out = imports.filter(i => i[0].data.name === d.data.name)
        d.in = imports.filter(i => i[i.length - 1].data.name === d.data.name)
      })      

      return nodes
    }

    function buildLines(data){
      var line = d3.lineRadial()
      .curve(d3.curveBundle.beta(0.85))
      .radius(function(d) { return d.y; })
      .angle(function(d) { return d.x / 180 * Math.PI; });

       return data.map(function(d) { 
        d.target = d[d.length - 1] 
        d.source = d[0] 
        return line(d)
      })
    }


    function over(event, d) {
      const pathsInLines = buildLines(d.in) 
      const pathsOutLines = buildLines(d.out)

      d3.select(this).attr("font-weight", "bold")
      d3.selectAll("path").filter(function (d){ return pathsInLines.includes(d3.select(this).attr("d"))})
        .attr("stroke","#D60014")
        .attr("stroke-opacity", 1)
        .attr("stroke-width", 2)
        .raise()
      d3.selectAll("path").filter(function (d){ return pathsOutLines.includes(d3.select(this).attr("d"))})
        .attr("stroke","#062296")
        .attr("stroke-opacity", 1)
        .attr("stroke-width", 2)
        .raise()
     
    }

    function out(event, d) {
      const pathsInLines = buildLines(d.in) 
      const pathsOutLines = buildLines(d.out)

      d3.select(this).attr("font-weight", null)

      d3.selectAll("path").filter(function (d){ return pathsInLines.includes(d3.select(this).attr("d"))})
        .attr("stroke","#FFC641")
        .attr("stroke-opacity", 0.12)
      d3.selectAll("path").filter(function (d){ return pathsOutLines.includes(d3.select(this).attr("d"))})
        .attr("stroke","#FFC641")
        .attr("stroke-opacity", 0.12)
    }
 
    function render(data){
      const diameter = 1200
      const radius = diameter / 2
      const innerRadius = radius - 180;
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
      const importsPaths = packageImports(root.leaves())
      const finalRoot = dataOrder(root.leaves(), importsPaths)

      cluster(root);
  
  
      link.data(importsPaths)
        .enter().append("path")
          .each(function(d) { d.source = d[0], d.target = d[d.length - 1] })
          .attr("class", "link")
          .attr("d", line)
          .attr("stroke", "#FFC641")
          .attr("stroke-opacity", "0.08")
          .attr("font-weight", 100)
  
      node.data(finalRoot)
        .enter().append("text")
          .attr("class", "node")
          .attr("dy", "0.31em")
          .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
          .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
          .text(function(d) { return d.data.key; })
          .on(("mouseover"), over)
          .on(("mouseout"), out)
  
    }
  
    const url = "https://raw.githubusercontent.com/AndresRubianoM/exportVisualization/master/dataGraph.csv"
    
    d3.csv(url).then( data => {
        const correctData = []
        let imports = ""
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
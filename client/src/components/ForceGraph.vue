<template>
  <v-row align="center" justify="center">
    <div
      :style="{
        width: width + 'px',
        height: height + 'px',
        border: '2px solid blue'
      }"
    >
      <svg width="100%" height="100%" id="forceGraph-svg">
        <defs>
          <pattern
            id="innerGrid"
            :width="innerGridSize"
            :height="innerGridSize"
            patternUnits="userSpaceOnUse"
          >
            <rect
              width="100%"
              height="100%"
              fill="none"
              stroke="#CCCCCC7A"
              stroke-width="0.5"
            />
          </pattern>
          <pattern
            id="grid"
            :width="gridSize"
            :height="gridSize"
            patternUnits="userSpaceOnUse"
          >
            <rect
              width="100%"
              height="100%"
              fill="url(#innerGrid)"
              stroke="#CCCCCC7A"
              stroke-width="1.5"
            />
          </pattern>
        </defs>
      </svg>
    </div>
  </v-row> </template
>>

<script>
import * as d3 from "d3";

export default {
  props: ["data", "nodeNameA", "nodeNameB", "mergeFlag"],
  data() {
    return {
      width: 1500,
      height: 768,
      gridSize: 100,
      selections: {},
      simulation: null,
      forceProperties: {
        center: {
          x: 0.5,
          y: 0.5
        },
        charge: {
          enabled: true,
          strength: -2000, // could be controlled by slider
          distanceMin: 1,
          distanceMax: 2000
        },
        collide: {
          enabled: true,
          strength: 0.7,
          iterations: 1,
          radius: 35
        },
        forceX: {
          enabled: false,
          strength: 0.05,
          x: 0.5
        },
        forceY: {
          enabled: false,
          strength: 0.35,
          y: 0.5
        },
        link: {
          enabled: true,
          distance: 100,
          iterations: 1
        }
      }
    };
  },
  computed: {
    innerGridSize() {
      return this.gridSize / 10;
    },
    nodes() {
      return this.data.nodes;
    },
    links() {
      return this.data.links;
    },
    // These are needed for captions
    linkTypes() {
      const linkTypes = [];
      this.links.forEach(link => {
        if (linkTypes.indexOf(link.type) === -1) {
          linkTypes.push(link.type);
        }
      });
      return linkTypes.sort();
    },
    classes() {
      const classes = [];
      this.nodes.forEach(node => {
        if (classes.indexOf(node.class) === -1) {
          classes.push(node.class);
        }
      });
      return classes.sort();
    }
  },
  created() {
    this.width = window.innerWidth - 500;
    this.height = window.innerHeight - 300;

    this.simulation = d3
      .forceSimulation()
      .force("link", d3.forceLink())
      .force("charge", d3.forceManyBody())
      .force("collide", d3.forceCollide())
      .force("center", d3.forceCenter())
      .force("forceX", d3.forceX())
      .force("forceY", d3.forceY())
      .on("tick", this.tick);
    this.updateForces();
  },
  mounted() {
    this.selections.svg = d3.select(this.$el.querySelector("svg"));
    const svg = this.selections.svg;

    // Add zoom and panning triggers
    this.zoom = d3
      .zoom()
      .scaleExtent([1 / 4, 4])
      .on("zoom", this.zoomed);
    svg.call(this.zoom);

    // Background grid
    // The width and height depends on the minimum scale extent and
    // the + 10% and negative index to create an infinite grid feel
    this.selections.grid = svg
      .append("rect")
      .attr("x", "-10%")
      .attr("y", "-10%")
      .attr("width", "410%")
      .attr("height", "410%")
      .attr("fill", "url(#grid)");

    this.selections.graph = svg.append("g");

    // Node and link count
    this.selections.statsNodes = svg
      .append("text")
      .attr("x", "1%")
      .attr("y", "96%")
      .attr("text-anchor", "left");

    this.selections.statsConnections = svg
      .append("text")
      .attr("x", "1%")
      .attr("y", "98%")
      .attr("text-anchor", "left");

    // Caption
    this.selections.caption = svg.append("g");
    this.selections.caption
      .append("rect")
      .attr("width", "200")
      .attr("height", "0")
      .attr("rx", "10")
      .attr("ry", "10")
      .attr("class", "caption");
  },
  methods: {
    getRandomBlue(d) {
      if (d.value < 5) return "#b0e4ff";
      else if (d.value < 30) return "#8cd7ff";
      else if (d.value < 40) return "#66caff";
      else if (d.value < 50) return "#1cb0ff";
      else return "#00a4fc";
    },
    tick() {
      // If no data is passed to the Vue component, do nothing
      if (!this.data) {
        return;
      }
      const transform = d => {
        return "translate(" + d.x + "," + d.y + ")";
      };

      const link = d => {
        return (
          "M" +
          d.source.x +
          "," +
          d.source.y +
          " L" +
          d.target.x +
          "," +
          d.target.y
        );
      };

      const graph = this.selections.graph;
      graph.selectAll("path").attr("d", link);
      graph.selectAll("circle").attr("transform", transform);
      graph.selectAll("text").attr("transform", transform);

      this.updateNodeLinkCount();
    },
    highlightToBeMerged() {
      const graph = this.selections.graph;

      switch (this.mergeFlag) {
        case true: {
          graph
            .selectAll("circle")
            .filter(d => {
              return d.name === this.nodeNameA;
            })
            .attr("class", "redd");

          graph
            .selectAll("circle")
            .filter(d => {
              return d.name === this.nodeNameB;
            })
            .attr("class", "greenn");
          break;
        }
        case false: {
          graph
            .selectAll("circle")
            .filter(d => {
              return d.name === this.nodeNameA;
            })
            .attr("class", d => d.class);

          graph
            .selectAll("circle")
            .filter(d => {
              return d.name === this.nodeNameB;
            })
            .attr("class", d => d.class);
          break;
        }
      }
    },
    updateData() {
      this.simulation.nodes(this.nodes);
      this.simulation.force("link").links(this.links);

      const simulation = this.simulation;
      const graph = this.selections.graph;

      // Links should only exit if not needed anymore
      graph
        .selectAll("path")
        .data(this.links)
        .exit()
        .remove();

      graph
        .selectAll("path")
        .data(this.links)
        .enter()
        .append("path")
        .attr("class", d => "link " + d.type)
        .attr("stroke", d => this.getRandomBlue(d)) // "#007bff")
        .attr("stroke-width", 1); // d => Math.sqrt(d.value*2,5))//d => Math.sqrt(d.value)) this is for strength dependant link width

      // Redrawing nodes to avoid lines above them
      graph.selectAll("circle").remove();
      graph
        .selectAll("circle")
        .data(this.nodes)
        .enter()
        .append("circle")
        .attr("r", 30)
        .attr("class", d => d.class)
        .call(
          d3
            .drag()
            .on("start", this.nodeDragStarted)
            .on("drag", this.nodeDragged)
            .on("end", this.nodeDragEnded)
        )
        .on("mouseover", this.nodeMouseOver)
        .on("mouseout", this.nodeMouseOut)
        .on("click", this.nodeClick);

      graph.selectAll("text").remove();
      graph
        .selectAll("text")
        .data(this.nodes)
        .enter()
        .append("text")
        .attr("x", 0)
        .attr("y", ".31em")
        .attr("text-anchor", "middle")
        .text(d => d.name);

      // Deleting merged nodes
      graph
        .selectAll("circle")
        .data(this.nodes)
        .filter(function(d) {
          return d.name === "123";
        })
        .remove();

      graph
        .selectAll("text")
        .data(this.nodes)
        .filter(function(d) {
          return d.name === "123";
        })
        .remove();

      // Update caption every time data changes
      this.updateCaption();
      simulation.alpha(1).restart();
    },
    updateForces() {
      const { simulation, forceProperties, width, height } = this;
      simulation
        .force("center")
        .x(width * forceProperties.center.x)
        .y(height * forceProperties.center.y);
      simulation
        .force("charge")
        .strength(
          forceProperties.charge.strength * forceProperties.charge.enabled
        )
        .distanceMin(forceProperties.charge.distanceMin)
        .distanceMax(forceProperties.charge.distanceMax);
      simulation
        .force("collide")
        .strength(
          forceProperties.collide.strength * forceProperties.collide.enabled
        )
        .radius(forceProperties.collide.radius)
        .iterations(forceProperties.collide.iterations);
      simulation
        .force("forceX")
        .strength(
          forceProperties.forceX.strength * forceProperties.forceX.enabled
        )
        .x(width * forceProperties.forceX.x);
      simulation
        .force("forceY")
        .strength(
          forceProperties.forceY.strength * forceProperties.forceY.enabled
        )
        .y(height * forceProperties.forceY.y);
      simulation
        .force("link")
        .distance(forceProperties.link.distance)
        .iterations(forceProperties.link.iterations);

      // updates ignored until this is run
      // restarts the simulation (important if simulation has already slowed down)
      simulation.alpha(1).restart();
    },
    updateNodeLinkCount() {
      let nodeCount = this.nodes.length;
      let linkCount = this.links.length;

      const highlightedNodes = this.selections.graph.selectAll(
        "circle.highlight"
      );
      const highlightedLinks = this.selections.graph.selectAll(
        "path.highlight"
      );
      if (highlightedNodes.size() > 0 || highlightedLinks.size() > 0) {
        nodeCount = highlightedNodes.size();
        linkCount = highlightedLinks.size();
      }
      this.selections.statsNodes.text("Nodes: " + nodeCount);
      this.selections.statsConnections.text("Connections: " + linkCount);
    },
    updateCaption() {
      const lineHeight = 30;
      const lineMiddle = lineHeight / 2;
      const captionXPadding = 28;
      const captionYPadding = 5;

      const caption = this.selections.caption;
      caption
        .select("rect")
        .attr(
          "height",
          captionYPadding * 2 +
            lineHeight * (this.classes.length + this.linkTypes.length)
        );

      const linkLine = d => {
        const source = {
          x: captionXPadding + 13,
          y:
            captionYPadding +
            (lineMiddle + 1) +
            lineHeight * this.linkTypes.indexOf(d)
        };
        const target = {
          x: captionXPadding - 10
        };
        return "M" + source.x + "," + source.y + "H" + target.x;
      };

      caption.selectAll("g").remove();
      const linkCaption = caption.append("g");
      linkCaption
        .selectAll("path")
        .data(this.linkTypes)
        .enter()
        .append("path")
        .attr("d", linkLine)
        .attr("class", d => "link " + d);

      linkCaption
        .selectAll("text")
        .data(this.linkTypes)
        .enter()
        .append("text")
        .attr("x", captionXPadding + 20)
        .attr(
          "y",
          d =>
            captionYPadding +
            (lineMiddle + 5) +
            lineHeight * this.linkTypes.indexOf(d)
        )
        .attr("class", "caption")
        .text(d => d);

      const classCaption = caption.append("g");
      classCaption
        .selectAll("circle")
        .data(this.classes)
        .enter()
        .append("circle")
        .attr("r", 10)
        .attr("cx", captionXPadding - 2)
        .attr(
          "cy",
          d =>
            captionYPadding +
            lineMiddle +
            lineHeight * (this.linkTypes.length + this.classes.indexOf(d))
        )
        .attr("class", d => d.toLowerCase());

      classCaption
        .selectAll("text")
        .data(this.classes)
        .enter()
        .append("text")
        .attr("x", captionXPadding + 20)
        .attr(
          "y",
          d =>
            captionYPadding +
            (lineMiddle + 5) +
            lineHeight * (this.linkTypes.length + this.classes.indexOf(d))
        )
        .attr("class", "caption")
        .text(d => d);

      const captionWidth = caption.node().getBBox().width;
      const captionHeight = caption.node().getBBox().height;
      const paddingX = 18;
      const paddingY = 12;
      caption.attr(
        "transform",
        "translate(" +
          (this.width - captionWidth - paddingX) +
          ", " +
          (this.height - captionHeight - paddingY) +
          ")"
      );
    },
    zoomed() {
      const transform = d3.event.transform;
      // The trick here is to move the grid in a way that the user doesn't perceive
      // that the axis aren't really moving
      // The actual movement is between 0 and gridSize only for x and y
      const translate =
        (transform.x % (this.gridSize * transform.k)) +
        "," +
        (transform.y % (this.gridSize * transform.k));
      this.selections.grid.attr(
        "transform",
        "translate(" + translate + ") scale(" + transform.k + ")"
      );
      this.selections.graph.attr("transform", transform);
    },
    nodeDragStarted(d) {
      if (!d3.event.active) {
        this.simulation.alphaTarget(0.3).restart();
      }
      d.fx = d.x;
      d.fy = d.y;
    },
    nodeDragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    },
    nodeDragEnded(d) {
      if (!d3.event.active) {
        this.simulation.alphaTarget(0.0001);
      } // could be a slider
      d.fx = null;
      d.fy = null;
    },
    nodeMouseOver(d) {
      const graph = this.selections.graph;
      const circle = graph.selectAll("circle");
      const path = graph.selectAll("path");
      const text = graph.selectAll("text");

      const related = [];
      const relatedLinks = [];
      related.push(d);
      this.simulation
        .force("link")
        .links()
        .forEach(link => {
          if (link.source === d || link.target === d) {
            relatedLinks.push(link);
            if (related.indexOf(link.source) === -1) {
              related.push(link.source);
            }
            if (related.indexOf(link.target) === -1) {
              related.push(link.target);
            }
          }
        });
      circle.classed("faded", true);
      circle.filter(df => related.indexOf(df) > -1).classed("highlight", true);
      path.classed("faded", true);
      path
        .filter(df => df.source === d || df.target === d)
        .classed("highlight", true);
      text.classed("faded", true);
      text.filter(df => related.indexOf(df) > -1).classed("highlight", true);
      // This ensures that tick is called so the node count is updated
      this.simulation.alphaTarget(0.0001).restart();
    },
    nodeMouseOut() {
      const graph = this.selections.graph;
      const circle = graph.selectAll("circle");
      const path = graph.selectAll("path");
      const text = graph.selectAll("text");

      circle.classed("faded", false);
      circle.classed("highlight", false);
      path.classed("faded", false);
      path.classed("highlight", false);
      text.classed("faded", false);
      text.classed("highlight", false);
      // This ensures that tick is called so the node count is updated
      this.simulation.restart();
    },
    nodeClick(d) {
      const circle = this.selections.graph.selectAll("circle");
      circle.classed("selected", false);
      circle.filter(td => td === d).classed("selected", true);
    }
  },
  watch: {
    data: {
      handler() {
        this.updateData();
      },
      deep: true
    },
    forceProperties: {
      handler() {
        this.updateForces();
      },
      deep: true
    },
    mergeFlag: {
      handler() {
        this.highlightToBeMerged();
      },
      deep: true
    }
  }
};
</script>
>

<style>
.faded {
  opacity: 0.1;
  transition: 0.2s opacity;
}
.highlight {
  opacity: 1;
}

/*path.link {
    fill: none;
    stroke: #666;
    stroke-width: 1.5px;
  }
  path.link.dotted {
    stroke: #005900;
    stroke-dasharray: 5, 2;
  }
  path.link.straight {
    stroke: #7f3f00;
  }*/

circle {
  fill: #001aff;
  stroke: #191900;
  stroke-width: 1.5px;
}
circle.rare {
  fill: #5cd1ff;
  stroke: #001900;
}
circle.normal {
  fill: #0093ce;
  stroke: #001900;
}
circle.frequent {
  fill: #003f58;
  stroke: #001900;
}

circle.redd {
  fill: red;
  stroke: #001900;
}

circle.greenn {
  fill: green;
  stroke: #001900;
}

circle.selected {
  stroke: rgb(0, 0, 0);
  stroke-width: 1px;
  animation: selected 0.5s 4 alternate ease-in-out;
}

@keyframes selected {
  from {
    stroke-width: 1px;
    r: 30;
  }
  to {
    stroke-width: 5px;
    r: 31;
  }
}

text {
  font: 10px arial;
  pointer-events: none;
  text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;
}

rect.caption {
  fill: #ccccccac;
  stroke: #666;
  stroke-width: 1px;
}
text.caption {
  font-size: 14px;
  font-weight: bold;
}
</style>

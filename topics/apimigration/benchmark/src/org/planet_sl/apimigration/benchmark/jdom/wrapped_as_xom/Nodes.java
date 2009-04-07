package org.planet_sl.apimigration.benchmark.jdom.wrapped_as_xom;

import static org.planet_sl.apimigration.benchmark.jdom.wrapped_as_xom.Utils.content2node;
import static org.planet_sl.apimigration.benchmark.jdom.wrapped_as_xom.Utils.node2content;

import java.util.List;

import org.planet_sl.apimigration.benchmark.anno.MapsTo;

@SuppressWarnings("unchecked")
@MapsTo("java.util.List")
public class Nodes {

	List list;
	
	Nodes(List list) {
		this.list = list;
	}
	
	@MapsTo("java.util.Collections.emptyList()")
	public Nodes() {
		this(java.util.Collections.emptyList());
	}

	@MapsTo("java.util.Collections.singletonList(Object)")
	public Nodes(Element test) {
		this(java.util.Collections.singletonList(test));
	}

	@MapsTo("java.util.List#add(Object)")
	public void append(Node node) {
		list.add(node2content(node));
	}

	@MapsTo("java.util.List#contains(Object)")
	public boolean contains(Node node) {
		return list.contains(node2content(node));
	}

	@MapsTo("java.util.List#get(int)")
	public Node get(int index) {
		return content2node((org.jdom.Content)list.get(index));
	}

	@MapsTo("java.util.List#add(int,Object)")
	public void insert(Node node, int index) {
		list.add(index, node2content(node));
	}

	@MapsTo("java.util.List#remove(int)")
	public Node remove(int index) {
		return (Node)content2node((org.jdom.Content)list.remove(index));
	}

	@MapsTo("java.util.List#size()")
	public int size() {
		return list.size();
	}

}
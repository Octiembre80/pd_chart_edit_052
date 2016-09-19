# -*- coding: utf-8 -*-

import pandas
import copy


_pd2hc_kind = {
    "bar": "column",
    "barh": "bar",
    "area": "area",
    "line": "line",
    "pie": "pie"
}


def pd2hc_kind(kind):
    if kind not in _pd2hc_kind:
        raise ValueError("%(kind)s plots are not yet supported" % locals())
    return _pd2hc_kind[kind]

_pd2hc_linestyle = {
    "-": "Solid",
    "--": "Dash",
    "-.": "DashDot",
    ":": "Dot"
}


def pd2hc_linestyle(linestyle):
    if linestyle not in _pd2hc_linestyle:
        raise ValueError("%(linestyle)s linestyles are not yet supported" % locals())
    return _pd2hc_linestyle[linestyle]


def json_encode(obj):
    return pandas.io.json.dumps(obj)


def serialize(df, output_type="javascript", chart_type="default", *args, **kwargs):
    def serialize_chart(df, output, *args, **kwargs):
        output["chart"] = {}
        if 'render_to' in kwargs:
            output['chart']['renderTo'] = kwargs['render_to']
        if "figsize" in kwargs:
            #if not kwargs["figsize"][0] == 0:   # When ommitted in the run.py is sent as (0,0). This helps standarazing the request for many charts.
                output["chart"]["width"] = kwargs["figsize"][0]
                output["chart"]["height"] = kwargs["figsize"][1]
        if "kind" in kwargs:
            output["chart"]["type"] = pd2hc_kind(kwargs["kind"])
        if kwargs.get('polar'):
            output['chart']['polar'] = True
            
    def serialize_colors(df, output, *args, **kwargs):
        pass
##        output ['chart']['colors']= {'#ff6d22','#002699','#00c788','#e0119d','#ea2839','#00b9e4','#fedf00','#0018ab','#81dd00','#bfbfbf'}
#        output["chart"]['backgroundColor']= {
#                'linearGradient': [0, 0, 200, 200],
#                'stops': [
#                    [0, 'rgb(255, 255, 255)'],
#                    [1, 'rgb(240, 240, 255)']
#                    ]
#            }
#    
##        output["chart"]['borderWidth]'={ 2,
##            'plotBackgroundColor': 'rgba(255, 255, 255, .9)',
##            'plotShadow': kwargs.get("TrickforTrue", True),
##            'plotBorderWidth': 1
##        }

    def serialize_credits(df, output, *args, **kwargs):
        output["credits"] = {
            "enabled" : kwargs.get("credits", False)
           }

    def serialize_data(df, output, *args, **kwargs):
        pass

    def serialize_drilldown(df, output, *args, **kwargs):
        pass

    def serialize_exporting(df, output, *args, **kwargs):
        pass

    def serialize_labels(df, output, *args, **kwargs):
        pass


    def serialize_legend(df, output, *args, **kwargs):
        output["legend"] = {
            "enabled": kwargs.get("legend", True),

            'align': 'right',
            'x': -10,
            'verticalAlign': 'top',
            'y': 30,
            'floating': kwargs.get("floating", True),

            'backgroundColor': 'white',
            'borderColor': '#CCC',
            'borderWidth': 1,
            'itemStyle': {'fontSize':'10px'},
            #'itemWidth': 80,
            #'adjustChartSize': kwargs.get("adjustChartSize", True),
            'shadow': kwargs.get("shadow", False)
        }

    def serialize_loading(df, output, *args, **kwargs):
        pass

    def serialize_navigation(df, output, *args, **kwargs):
        pass

    def serialize_noData(df, output, *args, **kwargs):
        pass

    def serialize_pane(df, output, *args, **kwargs):
        pass

    def serialize_plotOptions(df, output, *args, **kwargs): 
        output["plotOptions"] = {}        
        output["plotOptions"]["series"]={}

       
        if 'stacking' in kwargs:  
            output["plotOptions"]["series"] =  {'stacking': "normal"}
        
        if 'dataLabels' in kwargs: 
            output["plotOptions"]["series"]["dataLabels"] =  {'enabled': kwargs.get("dataLabels", True)
#                                                        'color': 'white',
#                                                        'style': {
#                                                        'textShadow': '0 0 3px white'
#                                                                }
                                                        }       
#        if 'click' in kwargs:
#             output["plotOptions"]["series"]['point']= {
#                           
#                                'events': {'''
#                                    click: function() {
#                                        if(this.x != UNDEFINED) {
#                                        	var get_members = $.post('/api/coverage/map',{series:this.series.name,category:this.category})
#	                                        	get_members.done(function( data ) {
#	                                        		members=jQuery.parseJSON(data);
#	                                           		$("#constituentsTable").empty();
#                  											        var tr;
#                  											        for (var i = 0; i < members.length; i++) {
#                  											            tr = $('<tr/>');
#                  											            tr.append("<td>" + members[i] + "</td>");
#                  											            $('#constituentsTable').append(tr);
#                  											        }
#	                                           });
#                                        }
#                                    }
#                                '''}
#                            
#                            }
        
        
    def serialize_series(df, output, *args, **kwargs):
        def is_secondary(c, **kwargs):
            return c in kwargs.get("secondary_y", [])
        if kwargs.get('sort_columns'):
            df = df.sort_index()
        series = df.to_dict('series')
        output["series"] = []
        for name, data in series.items():
            if df[name].dtype.kind in "biufc":
                sec = is_secondary(name, **kwargs)
                d = {
                    "name": name if not sec or not kwargs.get("mark_right", True) else name + " (right)",
                    "yAxis": int(sec),
                    "data": list(zip(df.index, data.values.tolist()))
                }
                if kwargs.get('polar'):
                    d['data'] = [v for k, v in d['data']]
                if kwargs.get("kind") == "area" and kwargs.get("stacked", True):
                    d["stacking"] = 'normal'
                if kwargs.get("style"):
                    d["dashStyle"] = pd2hc_linestyle(kwargs["style"].get(name, "-"))
                output["series"].append(d)
        output['series'].sort(key=lambda s: s['name'])

    def serialize_subtitle(df, output, *args, **kwargs):
        pass

    def serialize_title(df, output, *args, **kwargs):
        if "title" in kwargs:
            output["title"] = {"text": kwargs["title"]}
#            output["title"] = {"floating": kwargs.get("floating", True)}
        else:
            output["title"] = {"text": df.index.name}
#            output["title"] = {"floating": kwargs.get("floating", True)}

    def serialize_tooltip(df, output, *args, **kwargs):
        if 'tooltip' in kwargs:
            output['tooltip'] = kwargs['tooltip']
#            output['tooltip'] = {'headerFormat': '<b>{point.x}</b><br/>',
#                                 'pointFormat': '{series.name}: {point.y}<br/>Total: {point.stackTotal}'}
    def serialize_xAxis(df, output, *args, **kwargs):
        output["xAxis"] = {}
        
        #if kwargs.get("grid"):
        output["xAxis"]["gridLineWidth"] = 1
        output["xAxis"]["gridLineDashStyle"] = "Dot"
#            output["xAxis"]["gridLineInterpolation"] = "polygon"
#            output["xAxis"]["tickInterval"]=1
#            output["xAxis"]["minorGridLineWidth"]='0.3'
#            output["xAxis"]["minorTickInterval"]="auto"        
        
        
        if df.index.name:
            output["xAxis"]["title"] = {"text": df.index.name}
        if df.index.dtype.kind in "M":
            output["xAxis"]["type"] = "datetime"
        if df.index.dtype.kind == 'O':
            output['xAxis']['categories'] = sorted(list(df.index)) if kwargs.get('sort_columns') else list(df.index)          
        if kwargs.get("loglog") or kwargs.get("logx"):
            output["xAxis"]["type"] = 'logarithmic'
        if "xlim" in kwargs:
            output["xAxis"]["min"] = kwargs["xlim"][0]
            output["xAxis"]["max"] = kwargs["xlim"][1]
        if "rot" in kwargs:
            output["xAxis"]["labels"] = {"rotation": kwargs["rot"]}
        if "fontsize" in kwargs:
            output["xAxis"].setdefault("labels", {})["style"] = {"fontSize": kwargs["fontsize"]}
        if "xticks" in kwargs:
            output["xAxis"]["tickPositions"] = kwargs["xticks"]

    def serialize_yAxis(df, output, *args, **kwargs):
        yAxis = {}
        
        #if kwargs.get("grid"):
        yAxis["gridLineWidth"] = 1
        yAxis["gridLineDashStyle"] = "Dot"
        yAxis["minorGridLineWidth"]='0.3'
        yAxis["minorTickInterval"]="auto"
        
        if 'stackLabels' in kwargs:
            yAxis['stackLabels']= {'enabled': kwargs.get("stackLabels", True)}  
                         
        if kwargs.get("loglog") or kwargs.get("logy"):
            yAxis["type"] = 'logarithmic'
        if "ylim" in kwargs:
            yAxis["min"] = kwargs["ylim"][0]
            yAxis["max"] = kwargs["ylim"][1]
        if "rot" in kwargs:
            yAxis["labels"] = {"rotation": kwargs["rot"]}
        if "fontsize" in kwargs:
            yAxis.setdefault("labels", {})["style"] = {"fontSize": kwargs["fontsize"]}
        if "yticks" in kwargs:
            yAxis["tickPositions"] = kwargs["yticks"]
        output["yAxis"] = [yAxis]
        if kwargs.get("secondary_y"):
            yAxis2 = copy.deepcopy(yAxis)
            yAxis2["opposite"] = True
            output["yAxis"].append(yAxis2)

    def serialize_zoom(df, output, *args, **kwargs):
        if "zoom" in kwargs:
            if kwargs["zoom"] not in ("x", "y", "xy"):
                raise ValueError("zoom must be in ('x', 'y', 'xy')")
            output["chart"]["zoomType"] = kwargs["zoom"]

    output = {}
    df_copy = copy.deepcopy(df)
    if "x" in kwargs:
        df_copy.index = df_copy.pop(kwargs["x"])
    if kwargs.get("use_index", True) is False:
        df_copy = df_copy.reset_index()
    if "y" in kwargs:
        df_copy = pandas.DataFrame(df_copy, columns=kwargs["y"])
    serialize_chart(df_copy, output, *args, **kwargs)
    serialize_colors(df_copy, output, *args, **kwargs)
    serialize_credits(df_copy, output, *args, **kwargs)
    serialize_data(df_copy, output, *args, **kwargs)
    serialize_drilldown(df_copy, output, *args, **kwargs)
    serialize_exporting(df_copy, output, *args, **kwargs)
    serialize_labels(df_copy, output, *args, **kwargs)
    serialize_legend(df_copy, output, *args, **kwargs)
    serialize_loading(df_copy, output, *args, **kwargs)
    serialize_navigation(df_copy, output, *args, **kwargs)
    serialize_noData(df_copy, output, *args, **kwargs)
    serialize_pane(df_copy, output, *args, **kwargs)
    serialize_plotOptions(df_copy, output, *args, **kwargs)
    serialize_series(df_copy, output, *args, **kwargs)
    serialize_subtitle(df_copy, output, *args, **kwargs)
    serialize_title(df_copy, output, *args, **kwargs)
    serialize_tooltip(df_copy, output, *args, **kwargs)
    serialize_xAxis(df_copy, output, *args, **kwargs)
    serialize_yAxis(df_copy, output, *args, **kwargs)
    serialize_zoom(df_copy, output, *args, **kwargs)
    
    f = open('outputCore.txt','w')
    f.write(json_encode(output))
    f.close()     
    
    
    if output_type == "dict":
        return output
    if output_type == "json":
        return json_encode(output)
    if chart_type == "stock":
        return "new Highcharts.StockChart(%s);" % json_encode(output)
    return "new Highcharts.Chart(%s);" % json_encode(output)

#        return ["new Highcharts.StockChart(%s);" % json_encode(output),output ]
#    return ["new Highcharts.Chart(%s);" % json_encode(output),output ]

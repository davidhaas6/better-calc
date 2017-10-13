def dark_mode():
    import Foundation
    return Foundation.NSUserDefaults.standardUserDefaults().persistentDomainForName_(Foundation.NSGlobalDomain).objectForKey_("AppleInterfaceStyle") == "Dark"

def centered_text(html, hint_text=""):
	text_color = "white" if dark_mode() else "black"
	base = u"""
		<style>
		html, body {
			margin: 0px;
			width: 100%;
			height: 100%;
			color: <!--COLOR-->;
			font-family: "HelveticaNeue";
		}
		body > #centered {
			display: table;
			width: 100%;
			height: 100%
		}
		body > #centered > div {
			display: table-cell;
			vertical-align: middle;
			text-align: center;
			font-size: x-large;
			line-height: 1.1;
			padding: 30px;
		}
		#hint {
			opacity: 0.5;
			font-weight: bold;
			font-size: small;
			position: absolute;
			left: 10px;
			right: 10px;
			bottom: 10px;
			text-align: center;
		}
        hr {
            display: block;
            margin-top: 1em;
            margin-bottom: 0.5em;
            margin-left: auto;
            margin-right: auto;

            border: 0;
            height: 1px;
            background-image: linear-gradient(to right, rgba(0, 0, 0, .10), rgba(0, 0, 0, 0.15), rgba(0, 0, 0, .10));
        }
        #exp{
            opacity: 0.6;
            font-size: 16pt;
            font-weight: lighter;
        }
        #ans{
            opacity: 0.95;
            font-size: 28pt;
            font-weight: normal;
        }
		</style>
		<body>
		<div id='centered'>
		<div>
			<!--HTML-->
		</div>
		</div>
		<div id='hint'>
		<!--HINT-->
		</div>
		</body>
	"""
	return base.replace("<!--COLOR-->", text_color).replace("<!--HTML-->", html).replace("<!--HINT-->", hint_text)

#version 330
in vec2 position;
uniform vec2 center;
uniform vec2 viewport;
uniform float scale;
uniform bool grid_enabled;
out vec4 output_color;
void main() {
    vec3 base=mix(vec3(0.033,0.051,0.083),vec3(0.055,0.082,0.123),(position.y+1.0)*0.5);
    float spacing=pow(10.0,floor(log(100.0/scale)/log(10.0)));
    vec2 world=position*viewport*0.5/scale+center;
    vec2 d=abs(fract(world/spacing+0.5)-0.5)*spacing*scale;
    float grid=(1.0-smoothstep(0.0,0.8,min(d.x,d.y)))*0.028;
    output_color=vec4(base+(grid_enabled ? vec3(grid) : vec3(0.0)),1.0);
}

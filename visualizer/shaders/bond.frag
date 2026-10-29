#version 330
in vec4 tint;
in float edge;
out vec4 output_color;
void main() {output_color=vec4(tint.rgb,tint.a*(1.0-smoothstep(0.65,1.0,abs(edge))));}

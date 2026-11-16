# Why PBR Matters

## BOPEN

C S Y E seventy-two seventy, Building Virtual Environments. Why PBR Matters Why describing a surface as measurements beats painting the light in, and what that buys a game.

## BIDEA

Jambo. This is Liam, in for Bear. P B R is often sold as more realistic graphics. The bigger payoff is practical: materials that hold up under any light.

## BDEFS

Four terms. P B R: physically based rendering, where materials are measurements. Albedo: base colour, with no light painted in. Roughness: how blurred the reflections are. Metallic: whether the surface behaves like a metal.

## B01

The older shortcut is to paint the light into the texture. On the left, the highlight and the shadow are part of the image. On the right, a P B R material is lit by the scene. Lit from the upper left, the two look much alike.

## B02

Now move the light. The P B R highlight follows it around the sphere. The painted highlight stays exactly where the painter put it, and the painted shadow ends up facing the sun.

## B03

Change the time of day and the gap gets worse. The P B R sphere turns orange at sunset and dims at night. The painted sphere ignores the light entirely, so it glows the same in every scene.

## B04

With P B R you describe a surface once. Plastic, gold and rubber keep reading as plastic, gold and rubber at noon, at sunset and in a dim room, because the light does the painting, not the texture.

## B05

P B R models also follow a rule from physics: a surface never sends out more light than it receives. These are brightness measurements taken across Godot renders. As roughness rises, the highlight spreads wider and its peak drops.

## B06

Measurements also travel between tools. A material made in Blender leaves through the G L T F format as base colour, metallic and roughness, and arrives in Godot as a Standard Material 3D. Nobody repaints it.

## B07

And because they are numbers, you can check them. Saved as a text file, a Godot material is a short list of values that a person, a test or an agent can read.

## B08

One warning. P B R does not rescue bad lighting. With nothing to reflect, a polished metal looks like black plastic. Give it a sky and it reads as metal again. Judge every material under the light it will really be seen in.

## BVDT

Let’s recap with Claude. Painted light breaks when the light moves. PBR materials hold up under any light. Rougher means a wider, dimmer highlight. Measurements travel between tools and can be checked. Liam, in for Bear.

## BHTF

In Godot, make two spheres: one unshaded with a highlight painted into its texture, and one with a Standard Material 3D. Predict what happens to each as you rotate a directional light all the way round. Then remove the sky and look at a metal sphere. Check two things: Only the PBR highlight follows the light. The metal needs something to reflect.

## BOUT

Why PBR Matters At Nik Bear Brown.
